#!/usr/bin/env python

import serial
import time
import math

import rospy
import roslib
import tf

import geometry_msgs.msg
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Quaternion

motor_left = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)
motor_right = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5)
motor_left.flushOutput()
motor_left.flushInput()

motor_right.flushOutput()
motor_right.flushInput()

wl = 0
wr = 0

wl_prev = 0
wr_prev = 0

left_ticks = 0
right_ticks = 0

left_ticks_prev = 0
right_ticks_prev = 0

x = 0
y = 0
theta = 0

def Serial_write(motor_serial,command):
    motor_serial.write(command+'\n\r')
    time.sleep(0.05)
    motor_serial.flushInput()
    motor_serial.flushOutput()
    
def Serial_read(motor_serial):
    motor_serial.write('P\n\r')
    time.sleep(0.05)
    count = motor_serial.readline()
    motor_serial.flushInput()
    motor_serial.flushOutput()
    ticks = ''
    for i in count:
        if i.isdigit() or i == '-':
            ticks=ticks+i
    if ticks!='':
        return int(ticks)
    else:
        return 0
        
def callback_vel(cmd_vel_data):
    try:
        vel_x = cmd_vel_data.linear.x
        vel_th = cmd_vel_data.angular.z
      
        if vel_x > 0.52:
            vel_x = 0.52
        if vel_x < -0.52:
            vel_x = -0.52

        if vel_th > 2:
            vel_th = 2
        if vel_th < -2:
            vel_th = -2

        if (vel_x == 0):#only turning
            vr = vel_th*0.30/2.0  #distance b/w 2 wheels = 30cm = 0.3 mtrs
            vl = (-1)*vr

        elif (vel_th == 0): #moving forward/backward
            vr = vel_x
            vl = vel_x

        else:   #both turn and move forward/backward
            vr = vel_x + (vel_th*0.3/2.0)
            vl = vel_x - (vel_th*0.3/2.0)

        vr = vr*9.5493/0.05  #velocity to RPM conversion
        vl = vl*9.5493/0.05  #wheel radius = 5cm = 0.05 mtrs

        vr = vr*2.55  #RPM to PWM conversion
        vl = vl*2.55

        if vr > 255:
            vr = 255
        if vr < -255:
            vr = -255

        if vl > 255:
            vl = 255
        if vl < -255:
            vl = -255
            
	global wl,wl_prev
	global wr,wr_prev

    	global left_ticks,right_ticks
   	global left_ticks_prev,right_ticks_prev
    	global x,y,theta
	
        wl = int(vl)
        wr = int(vr)
    
        if (wl!=wl_prev):
                wl = wl*-1  #because left motor spins backward for +ve PWM values
            	Serial_write(motor_left,'S'+str(wl))
            	wl_prev=wl

        if (wr!=wr_prev):
          	Serial_write(motor_right,'S'+str(wr))
            	wr_prev = wr

        left_ticks = Serial_read(motor_left)
        left_ticks = left_ticks*-1 #because left motor spins backward for +ve PWM values
            
        right_ticks = Serial_read(motor_right)
        
        Dl = (left_ticks-left_ticks_prev)*2*3.14159*5/(1800*100) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs
        Dr = (right_ticks-right_ticks_prev)*2*3.14159*5/(1800*100) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs

        left_ticks_prev = left_ticks
        right_ticks_prev = right_ticks

        Dc = (Dr+Dl)/2 
        theta = theta + (Dr-Dl)/0.3   #L = 30 cm distance between 2 wheels in mtrs
        x = x + Dc*math.cos(theta)
        y = y + Dc*math.sin(theta)

        odom = Vector3()
        odom.x = x
        odom.y = y
        odom.z = theta

        pyserial_odom.publish(odom)

        #Broadcasting the transform
    
        br = tf.TransformBroadcaster()
        odom_tran = TransformStamped()
        odom_quat = Quaternion()

        odom_quat = tf.transformations.quaternion_from_euler(0, 0, theta)
        odom_tran.header.frame_id = "odom"
        odom_tran.child_frame_id = "base_link"
        odom_tran.transform.translation.x = x
        odom_tran.transform.translation.y = y
        odom_tran.transform.translation.z = 0.0
        odom_tran.transform.rotation = odom_quat
        odom_tran.header.stamp = rospy.Time.now()
            
        br.sendTransform(odom_tran)
        rate.sleep()
            
    except rospy.ROSInterruptException: #when you press ctrl+c
        print rospy.ROSInterruptException
        pass
    
        
if __name__== '__main__':
    
    Serial_write(motor_left,"P0")
    Serial_write(motor_right,"P0")
    Serial_write(motor_left,"M255")
    Serial_write(motor_right,"M255")
    
    rospy.init_node('odometry_raw',anonymous=True)
    cmd_vel_sub = rospy.Subscriber("/cmd_vel",Twist, callback_vel)
    pyserial_odom = rospy.Publisher("/odometry_raw",Vector3, queue_size=10)
    rate = rospy.Rate(5)
    rospy.spin()
    
            
    
    
    
        


    
