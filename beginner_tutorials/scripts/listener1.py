#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import serial
import time
import datetime

rhino_serial = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5)    

rhino_serial.flushOutput()
rhino_serial.flushInput()

def Rhino_send(s):
    global rhino_serial
    rhino_serial.write(s+'\n\r')
    #time.sleep(0.2)
    rhino_serial.flushInput()
    rhino_serial.flushOutput()
'''
def Rhino_read(r):
    global rhino_serial
    rhino_serial.write(r +'\n\r')
    time.sleep(0.2)
    read = rhino_serial.readline()
    rhino_serial.flushInput()
    rhino_serial.flushOutput()
    a = ''
    for i in read:
        if i.isdigit() or i=='-':
            a=a+i
    if a!='':
        return int(a)
    else:
        return 0
''' 
def callback(data):
    p = data.data
    if(p[1]=='-'):
    	p1 = p[0] + p [2:]
    else:
    	p1 = p[:1] + '-' + p[1:]
    print(p1)	
    Rhino_send(p1)


def listener():

    rospy.init_node('listener1', anonymous=True)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
