#!/usr/bin/env python
#from __future__ import print_function
from models import object_detection
from config import config
import cv2
import tensorflow as tf
import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from depth.msg import cood
from cv_bridge import CvBridge, CvBridgeError

model_name = config.models["1"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.6)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IMAGE_SIZE = 320
class image_converter:
 
  def __init__(self):
    self.pub = rospy.Publisher('object',cood)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.callback)
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

#    cv2.imshow("image",cv_image)
    cv2.waitKey(3)

    with tf.device('/gpu:0'):
                frame = cv_image
                in_progress = net.get_status()
                if (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    k1 , n = net.predict(img=resize_frame, display_img=frame)
                else:
                    print '[Warning] drop frame or in progress'
    send = cood()
    send.n = n		
    for i in range(0,n):    
	k = k1[i]
	send.y.append( (k['bb_o'][0]+k['bb_o'][2])/2)
	send.x.append((k['bb_o'][1]+k['bb_o'][3])/2)
	send.c.append(k['class'])
    try:
      self.pub.publish(send)
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('kinect_object', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
