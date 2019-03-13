#!/usr/bin/env python

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
from geometry_msgs.msg import PointStamped  #For Encoder Data reception

# Initialize global variables for Odometry Calculation 
old_lt_count = 0
old_rt_count = 0
prev_time = None
x = 0
y = 0
theta = 0
dx = 0
dy = 0
delta_theta = 0

# Bot Parameters
    
wheel_radius = 0.0525
# Ticks per revolution
tpr = 29520
meters_per_count = 2*math.pi*wheel_radius/tpr
# To be measured
base_width = 0.3 + 0.032 # Correction Factor for BaseWidth from testing

# Define publisher handle
odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)

def callback(msg):
    global prev_time
    global old_rt_count
    global old_lt_count
    global x 
    global y
    global theta
    global dx
    global dy
    global delta_theta

    if prev_time == None:
        prev_time = msg.header.stamp
        old_lt_count = 1*msg.point.x
        old_rt_count = 1*msg.point.y
    else :
        cur_time = msg.header.stamp
        rt_count = 1*msg.point.y
        lt_count = 1*msg.point.x

        dt = (cur_time - prev_time).to_sec()

        vel = meters_per_count * (lt_count - old_lt_count)/dt
        ver = meters_per_count * (rt_count - old_rt_count)/dt

        delta_s = meters_per_count*(((rt_count - old_rt_count) + (lt_count - old_lt_count))/2.0)
        delta_theta = meters_per_count*(((rt_count - old_rt_count) - (lt_count - old_lt_count))/base_width)

        dx = delta_s * math.cos(theta + delta_theta / 2.0)
        dy = delta_s * math.sin(theta + delta_theta / 2.0)

        x += dx                                                                                      
        y += dy                                                                                     
        theta += delta_theta

        print theta*180/3.14

        # Convert euler to quat
        quaternion = tf.transformations.quaternion_from_euler(0, 0, -theta)

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
        br.sendTransform((-x, -y, 0),
             tf.transformations.quaternion_from_euler(0, 0, theta),
             rospy.Time.now(),
             "odom",
             "base_link")

        prev_time = cur_time
        old_lt_count = lt_count
        old_rt_count = rt_count

def main():

    rospy.init_node('OdomPublisher', anonymous=True)
    rospy.Subscriber("encoder", PointStamped, callback)
    rate = rospy.Rate(50)
    
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == "__main__":
    main()
