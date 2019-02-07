#!/usr/bin/env python
#looks like early version of Odometry_2
import serial
import time
import math

import rospy
import roslib
import geometry_msgs.msg
from geometry_msgs.msg import Vector3

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
        if i.isdigit():
            ticks=ticks+i
    if ticks!='':
        return int(ticks)
    else:
        return 0
        
def callback_vel(vel_data):
    try:
        #global wl,wr   
	global wl,wl_prev
	global wr,wr_prev

    	global left_ticks,right_ticks
   	global left_ticks_prev,right_ticks_prev

    	global x,y,theta           
        wl = int(vel_data.y)
        wr = int(vel_data.x)
	
    	odom = Vector3()
    
        if (wl!=wl_prev):
                wl = wl*-1
            	Serial_write(motor_left,'S'+str(wl))
            	wl_prev=wl

        if (wr!=wr_prev):
          	Serial_write(motor_right,'S'+str(wr))
            	wr_prev = wr

        left_ticks = Serial_read(motor_left)
        left_ticks = left_ticks*-1
        
        right_ticks = Serial_read(motor_right)
        
        Dl = (left_ticks-left_ticks_prev)*2*3.14159*5/(1800*1000) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs
        Dr = (right_ticks-right_ticks_prev)*2*3.14159*5/(1800*1000) #radius = 5cm #1800 ticks = 1 rev #dl in mtrs

	left_ticks_prev = left_ticks
	right_ticks_prev = right_ticks

	Dc = (Dr+Dl)/2 
	theta = theta + (Dr-Dl)/0.3 #L = 30 cm distance between 2 wheels in mtrs
	x = x + Dc*math.cos(theta)
	y = y + Dc*math.sin(theta)

	odom.x = x
	odom.y = y
	odom.z = theta

	pyserial_odom.publish(odom)
	rate.sleep()
    except:
        pass
        
if __name__== '__main__':
    Serial_write(motor_left,"P0")
    Serial_write(motor_right,"P0")
    rospy.init_node('odometry_raw',anonymous=True)
    motor_vel = rospy.Subscriber("/motor_vel",Vector3, callback_vel)
    pyserial_odom = rospy.Publisher("/odometry_raw",Vector3, queue_size=10)
    rate = rospy.Rate(5)
    rospy.spin()
    
    
        


    
