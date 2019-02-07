from sensor_msgs.msg import Image
import roslib
import sys
import rospy
from depth.msg import image2
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
    im = image2()
    def __init__(self):
        self.pub = rospy.Publisher('depth2',image2,queue_size=10)
        self.image_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.callback)
        self.depth_sub = rospy.Subscriber("/camera/depth_registered/image_raw",Image,self.dep_callback)

    """
    This is assuming that for each RGB, we have a Depth that is also sent
    If the RGB frequency is more, then, we have more RGB callbacks, with only the latest being taken
    This implies that the depth and RGB data may not coincide. One method would be to retain the 
    first RGB that is obtained, and also the first depth that is obtained, though that is also not
    guaranteed for now
    """
    def callback(self,data):
        global im
        try:
            im.rgb = data
            if im.d.height != 0:
                self.pub.publish(im)
                im = image2()
        except CvBridgeError as e:
            print(e)

    def dep_callback(self, data):
        global im
        try:
            im.d = data
            if im.rgb.height != 0:
                self.pub.publish(im)
                im = image2()
        except Exception as e:
            print e.message

def main(args):
    ic = image_converter()
    rospy.init_node('both_img', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)