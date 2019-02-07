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

import math

x = []
y = []
s = []
n = None
class image_converter:
 
  def __init__(self):
    self.pub = rospy.Publisher('coord_converter',cood ,queue_size=10)

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
    dist = []
    thet = []
    print type(n),n
    send = cood()
    if n==0 or n == None:
      return
    
    try:
      bridge = CvBridge()
      cv_image = bridge.imgmsg_to_cv2(data, "passthrough")
    except CvBridgeError as e:
      print(e)
    print(cv_image.shape)
    field_angle = math.radians((57 / 2.0))
    for l in range(0,n):
      x1 = int(x[l])
      y1 = int(y[l])
      x1 = x1*2 
      y1 = int(y1*1.5)
      
      print x1,y1
      dep = cv_image[y1][x1]
      X = dep * math.tan(field_angle)
      p = (320 - x1)
      x_small = p * X / 320.0
      theta = math.atan2(x_small, dep)
      r = math.sqrt(x_small**2 + dep**2)
      dist.append(r/1000.0)
      thet.append(theta)
      #cv2.line(cv_image,(x1,y1),(319,319),(255,0,0),5) 
      cv2.circle(cv_image, (x1,y1), 75, (0,255,0))
    cv2.imshow("Image window", cv_image)

    cv2.waitKey(3)
    #time.sleep(.111)    
    print "distances:", dist, "thetas:", thet, "object:", s
    send.x = dist
    send.y = thet
    send.c = s
    send.n =n
    try:
      self.pub.publish(send)
    except CvBridgeError as e:
      print(e)

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
