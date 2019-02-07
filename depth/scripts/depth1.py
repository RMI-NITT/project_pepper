#!/usr/bin/env python
import rospy
import cv2
import roslib
import sys

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
def callback(msg):
    x = msg.data
    h = msg.height
    w = msg.width
    s = msg.step
    print(w)   
    print(h)
    print(s)
    print(len(x))
    cv_image = bridge.imgmsg_to_cv2(x, desired_encoding="passthrough")
    print(cv_image)
    
def main():
    rospy.init_node('distance')
    rospy.Subscriber('/camera/rgb/image_color', Image , callback)
    rospy.spin()

if __name__ == '__main__':
    main()


#try with open cv rect image use karo
