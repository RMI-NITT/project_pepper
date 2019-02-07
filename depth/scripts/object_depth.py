#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('ros_to_cv_v2')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from depth.msg import cood

x=0
y=0
class image_depth:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_depth",Image, queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/depth/image",Image,self.callback)
    rospy.Subscriber("/object", cood, self.callback_depth)


  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
    except CvBridgeError as e:
      print(e)

    (rows,cols) = cv_image.shape
    print("rows:", rows, "cols:", cols)
    #if cols > 60 and rows > 60 :
     # cv2.circle(cv_image, (300,500), 25, (0,255,0))

    #for a in range(rows):
    pts1 = np.float32([[200,225],[300,225],[300,360],[200,360]])
    pts2 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(cv_image,M,(cols,rows))
    cv2.imshow("Perspective",img)

    print("depth", img[y][x]) #row is y and column is x
    cv2.circle(img, (x,y), 15, (0,255,0))
    print("at call back x:",x, "y:", y )
    cv2.imshow('depth image', img)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(img, "passthrough"))
    except CvBridgeError as e:
      print(e)

  def callback_depth(self, msg):
      #print("depth", img[msg.x][msg.y])
      #cv2.circle(img, (msg.x,msg.y), 15, (0,255,0))
      global x
      global y
      x=msg.x[0]
      y=msg.y[0]
      print("x:",x,"y:", y)


def main(args):

  ic = image_depth()
  rospy.init_node('image_depth', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
