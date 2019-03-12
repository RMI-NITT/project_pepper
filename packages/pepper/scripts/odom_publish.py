#!/usr/bin/env python
## For RHINO Motors ##
"""Script to publish odometry data"""
import serial
import math
import time

import rospy
import roslib
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist

def motor_serial_write(motor_serial, command):
    """Method to write the command to the motors

    :param motor_serial The serial port to write to
    :param command The command to issue to the motor
    """
    # P - Read write encoder position in Rhino Motor RMCS220x series
    motor_serial.write(command + "\n\r")
    # time.sleep(0.05)
    motor_serial.flushInput()
    motor_serial.flushOutput()


def motor_serial_read(motor_serial):
    """Method to read the data from the encoders

    :param motor_serial The serial port to read from
    """
    # This does something!
    motor_serial.write('P\n\r')
    # time.sleep(0.05)
    count = motor_serial.readline()
    motor_serial.flushInput()
    motor_serial.flushOutput()

    # Check if the input string is garbage
    # If NOT garbage, convert to int and return count
    ticks = ''
    for i in count:
        if i.isdigit() or i == '-':
            ticks = ticks + i
    if ticks != '':
        return int(ticks)
    else:
        return -1


def main():

    # Subject to change
    motor_left = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    motor_right = serial.Serial("/dev/ttyUSB1", 9600, timeout=0.5)

    motor_left.flushOutput()
    motor_right.flushOutput()
    motor_left.flushInput()
    motor_right.flushInput()

    time.sleep(1)
    print "Ready!"

    # Initialize the motors to 0 encoder value
    motor_serial_write(motor_left, "P0")
    motor_serial_write(motor_right, "P0")

    motor_serial_write(motor_left, "M200")
    motor_serial_write(motor_right, "M200")

    motor_serial_write(motor_left, "S100")
    motor_serial_write(motor_right, "S-100")

    print "Motor Setup Done"

    # Initialize variables for Odometry Calculation 
    x = 0
    y = 0
    theta = 0
    dx = 0
    dy = 0
    delta_theta = 0
    rt_count = 0
    lt_count = 0
    old_lt_count = 0
    old_rt_count = 0
    prev_time = None
    cur_time = 0

    # Bot Parameters
    
    wheel_radius = 0.0525
    # Ticks per revolution
    tpr = 1800
    meters_per_count = 2*math.pi*wheel_radius/tpr
    # To be measured
    base_width = 0.3 


    odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
    rospy.init_node('OdomPublisher', anonymous=True)
    rate = rospy.Rate(50)
    
    while True:
        try:
            if prev_time is None:
                dt = 10000
                cur_time = rospy.get_time()
                # Find better logic for initial dT
            else:

                cur_time = rospy.get_time()

                lt_count = motor_serial_read(motor_left)
                rt_count = motor_serial_read(motor_right)

                #lt_count *= -1
                rt_count *= -1
                
                dt = cur_time - prev_time

                vel = meters_per_count * (lt_count - old_lt_count)/dt
                ver = meters_per_count * (rt_count - old_rt_count)/dt

                delta_s = meters_per_count*(((rt_count - old_rt_count) + (lt_count - old_lt_count))/2.0)
                delta_theta = meters_per_count*(((rt_count - old_rt_count) - (lt_count - old_lt_count))/base_width)

                dx = delta_s * math.cos(theta + delta_theta / 2.0)
                dy = delta_s * math.sin(theta + delta_theta / 2.0)

                x += dx                                                                                      
                y += dy                                                                                      
                theta += delta_theta

                # Convert euler to quat
                quaternion = tf.transformations.quaternion_from_euler(0, 0, theta)

                # Populate ROS message
                pose = Pose()

                pose.position.x = x
                pose.position.y = y
                pose.position.z = 0

                pose.orientation.x = quaternion[0]
                pose.orientation.y = quaternion[1]
                pose.orientation.z = quaternion[2]
                pose.orientation.w = quaternion[3]

                twist = Twist()
                twist.linear.x = dx/dt
                twist.linear.y = dy/dt
                twist.linear.z = 0
                twist.angular.x = 0.0;
                twist.angular.y = 0.0;
                twist.angular.z = delta_theta / dt

                odom = Odometry()
                odom.header.stamp = rospy.Time.now()
                odom.header.frame_id = "world"
                odom.pose.pose = pose 
                odom.twist.twist = twist

                odom_pub.publish(odom)

                # Publish Odom Frame transform
                br = tf.TransformBroadcaster()
                br.sendTransform((x, y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, theta),
                     rospy.Time.now(),
                     "odom",
                     "base_link")

            prev_time = cur_time
            old_lt_count = lt_count
            old_rt_count = rt_count
            rate.sleep()

        except KeyboardInterrupt:
            print "shutting down motors"
            motor_serial_write(motor_left, "S0")
            motor_serial_write(motor_right, "S0")
            break

if __name__ == "__main__":
    main()
