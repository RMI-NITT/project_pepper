#!/usr/bin/env python

# Import the object detection modules
from models import object_detection
from config import config
import cv2
import tensorflow as tf
import roslib
#roslib.load_manifest('my_package')

# Import modules necessary for ros
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from depth.msg import cood
from cv_bridge import CvBridge, CvBridgeError
from depth.msg import image2

import math

# Global variable containing all the x, y, strings of all objects
x = []
y = []
s = []
n = None

model_name = config.models["1"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.6)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IMAGE_SIZE = 320

class image_processor:
    def __init__(self):
        self.pub = rospy.Publisher('coord_converter',cood ,queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/depth2",image2,self.callback)

    def callback(self, data):
        global x
        global y
        global s
        global n
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data.rgb, "bgr8")
        except CvBridgeError as e:
            print e
        cv2.waitKey(3)

        with tf.device('/gpu:0'):
                frame = cv_image
                in_progress = net.get_status()
                if (not in_progress):
                    resize_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
                    k1 , n = net.predict(img=resize_frame, display_img=frame)
                else:
                    print '[Warning] drop frame or in progress'
        for i in range(n):
            k = k1[i]
            y.append( (k['bb_o'][0]+k['bb_o'][2])/2)
            x.append((k['bb_o'][1]+k['bb_o'][3])/2)
            s.append(k['class'])

        # Processing of the depth data
        dist = []
        thet = []
        send = cood()
        if n==0 or n==None:
            return
        try:
            bridge = CvBridge()
            dep_img = bridge.imgmsg_to_cv2(data.d, "passthrough")
        except CvBridgeError as e:
            print e
        print dep_img.shape

        # Calculations for the coordinates begins
        field_angle = math.radians((57 / 2.0))
        for l in range(0,n):
            x1 = int(x[l])
            y1 = int(y[l])
            x1 = x1*2
            y1 = int(y1*1.5)

            print x1, y1
            dep = dep_img[y1][x1]
            X = dep * math.tan(field_angle)
            p = (320 - x1)
            x_small = p * X / 320.0
            theta = math.atan2(x_small, dep)
            r = math.sqrt(x_small**2 + dep**2)
            dist.append(r/1000.0)
            thet.append(theta)
            cv2.circle(dep_img, (x1,y1), 75, (0,255,0))
        cv2.imshow("Image window", dep_img)
        cv2.waitKey(3)

        print "distances:", dist, "thetas:", thet, "object:", s
        send.x = dist
        send.y = thet
        send.c = s
        send.n = n
        try:
            self.pub.publish(send)
        except CvBridgeError as e:
            print e

def main(args):
    ip = image_processor()
    rospy.init_node('im_proc', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down!"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)