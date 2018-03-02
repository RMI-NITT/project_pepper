#!/usr/bin/env python

import time
import math

import rospy
import roslib
import tf

import geometry_msgs.msg
import std_msgs.msg

from geometry_msgs.msg import Vector3

x = 0
y = 0
theta = 0
# TODO Rhino Read
prev_l = 0
prev_r = 0

if __name__== '__main__':
    
    global x,y,theta
    
    rospy.init_node('odometry_publish1',anonymous=True)
    pyserial_odom = rospy.Publisher("/odom_chumma",Vector3, queue_size=10)
    rate = rospy.Rate(5)
    
    while not rospy.is_shutdown():
        try:
            left_ticks = Serial_read(motor_left)
            left_ticks = left_ticks*-1 #because left motor spins backward for +ve PWM values
	             
            right_ticks = Serial_read(motor_right)
            
	    #print "Printing only the ticks - left, right"
            #print left_ticks, right_ticks
	    #print right_ticks - left_ticks

	    del_l = left_ticks - left_ticks_prev
            del_r = right_ticks - right_ticks_prev
            print del_l, del_r
	    if del_l < -1000 or del_l > 1000:
                continue
            
            if del_r < -1000 or del_r > 1000:
                continue

	    """
	    curr_diff = right_ticks - left_ticks
            del_diff = curr_diff - prev_diff
            if del_diff < -100 or del_diff > 100:
                continue
            prev_diff = curr_diff
	    """
            
            Dl = (left_ticks-left_ticks_prev)*2*3.14159*5/(1800*100) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs
            Dr = (right_ticks-right_ticks_prev)*2*3.14159*5/(1800*100) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs

            left_ticks_prev = left_ticks
            right_ticks_prev = right_ticks

            Dc = (Dr+Dl)/2.0
            x = x + Dc*math.cos(theta)
            y = y + Dc*math.sin(theta)
            theta = theta + (Dr-Dl)/(0.3)   #L = 30 cm distance between 2 wheels in mtrs


            odom = Vector3()
            odom.x = x
            odom.y = y
            odom.z = theta

            pyserial_odom.publish(odom)

            #Broadcasting the transform
	    '''
            br = tf2_ros.TransformBroadcaster()
            odom_tran = TransformStamped()
            odom_quat = Quaternion()

            odom_quat = tf.transformations.quaternion_from_euler(0, 0, theta)
            odom_tran.header.frame_id = "odom"
            odom_tran.header.stamp = rospy.Time.now()
            odom_tran.child_frame_id = "base_link"
            odom_tran.transform.translation.x = x
            odom_tran.transform.translation.y = y
            odom_tran.transform.translation.z = 0.0
            odom_tran.transform.rotation = odom_quat
            
            br.sendTransform(odom_tran)'''
            rate.sleep()      
            
        except rospy.ROSInterruptException: #when you press ctrl+c
            print (rospy.ROSInterruptException)
            pass
    
    
    
        

