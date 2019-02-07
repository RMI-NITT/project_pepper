#!/usr/bin/env python

import rospy
import roslib
import sys
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import geometry_msgs.msg

cv2.namedWindow('image')
cascade = cv2.CascadeClassifier("/home/prakash/catkin_ws/src/pepper/scripts/cascade.xml")

def detect(img, cascade):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    for scale in [float(i)/10 for i in range(11, 15)]:
        for neighbors in range(2,5):
            rects = cascade.detectMultiScale(img, scaleFactor=scale, minNeighbors=neighbors,minSize=(100, 100))       
    return rects


class image_converter:
  
    def __init__(self):
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.rgb_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.rgb_callback)  
        self.depth_sub = rospy.Subscriber("/camera/depth/image",Image,self.depth_callback)

        self.x = 0
        self.y = 0
            
    def rgb_callback(self,data):
        try:
            global cascade
            cv_rgb = self.bridge.imgmsg_to_cv2(data,"passthrough")
            rects = detect(cv_rgb,cascade)

            for (x,y,w,h) in rects:
                cv2.rectangle(cv_rgb,(x,y),(x+w,y+h),(255,255,0),2)
                self.x = x + (w/2)
                self.y = y + (h/2)
                    
            #self.x = rects[0] + (rects[2]/2)
            #self.y = rects[1] + (rects[3]/2)

            self.x = int(self.x)
            self.y = int(self.y)

            ros_img = self.bridge.cv2_to_imgmsg(cv_rgb, "bgr8")
            self.image_pub.publish(ros_img)
             
        except CvBridgeError, e:
            print e

    def depth_callback(self,data):
        try:       
            cv_depth = self.bridge.imgmsg_to_cv2(data,"passthrough")
            if self.x!=0:
                depth = cv_depth[self.y,self.x]
                print depth

        except CvBridgeError, e:
            print e

if __name__ == '__main__':    
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"
    cv2.destroyAllWindows()
