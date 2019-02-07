#!/usr/bin/env python
#subscribes /cmd_vel and writes the value in the motors
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


def Serial_write(motor_serial,command):
    motor_serial.write(command+'\n\r')
    time.sleep(0.05)
    motor_serial.flushInput()
    motor_serial.flushOutput()
    
#globals

wl = 0
wr = 0

wl_prev = 0
wr_prev = 0

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
       
        wl = int(vl)
        wr = int(vr)

        print wl,wr
        
        if (wl!=wl_prev):
                wl = wl*-1  #because left motor spins backward for +ve PWM values
            	Serial_write(motor_left,'S'+str(wl))
            	wl_prev=wl

        if (wr!=wr_prev):
          	Serial_write(motor_right,'S'+str(wr))
            	wr_prev = wr
            	
        rate.sleep()
        
    except rospy.ROSInterruptException:
        print (rospy.ROSInterruptException)
        pass

if __name__== '__main__':

    Serial_write(motor_left,"M255")
    Serial_write(motor_right,"M255")
    rospy.init_node('velocity_subscribe',anonymous=True)
    cmd_vel_sub = rospy.Subscriber("/cmd_vel",Twist, callback_vel)
    rate = rospy.Rate(5)
    rospy.spin()
