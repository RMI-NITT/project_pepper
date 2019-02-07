#!/usr/bin/env python
#from __future__ import print_function
 
import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from depth.msg import cood
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import numpy as np
x = []
y = []
s = []
n = None
class image_converter:
 
  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/depth_registered/image_raw",Image,self.callback)
    self.data = rospy.Subscriber("/object",cood,self.object_callback)
  
  def object_callback(self,data):
    global x
    global y
    global s
    global n
    x = data.x
    y = data.y
    s = data.c
    n = data.n
  
  def callback(self,data):
    global x
    global y
    global s
    global n
    d = []
    print type(n),n
    if n==0 or n == None:
      print("bleh")
      return
    
    try:
      bridge = CvBridge()
      cv1_image = bridge.imgmsg_to_cv2(data, "passthrough")
    except CvBridgeError as e:
      print(e)
    cv_image = cv2.resize(cv1_image, (320, 320))
    for l in range(0,n):
      x1 = int(x[l])
      y1 = int(y[l]) 
      print x1,y1
      d.append(cv_image[x1][y1]) 
      #cv2.line(cv_image,(x1,y1),(319,319),(255,0,0),5) 
      cv2.circle(cv_image, (x1,y1), 75, (0,255,0))
    cv2.imshow("Image window", cv_image)

    a = cv_image >= 2000
    #print a.shape
    b = []
    for i in range(a.shape[0]):
        b.append([])
        for j in range(a.shape[1]):
            if a[i][j] == True:
                b[i].append(1)
            else:
                b[i].append(0)

    for i in range(320):
        for j in range(320):
            print b[i][j], 
        print ""

    cv2.waitKey(3)
    print "depth:", d, "object:", s
    
    _ = raw_input("Printed!! Press enter to continue")
'''
    try:
      
    except CvBridgeError as e:
      print(e)
'''
def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)