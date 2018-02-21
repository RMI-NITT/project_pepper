#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
def callback(msg):
    x = msg.data
    print(x[1][1])
    
def main():
    rospy.init_node('distance')
    rospy.Subscriber('/camera/depth_registered/image_raw', Image , callback)
    rospy.spin()

if __name__ == '__main__':
    main()

