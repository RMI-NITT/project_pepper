import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style

import time

import rospy
from geometry_msgs.msg import Vector3

# Basic style of the plot
style.use('fivethirtyeight')

# Initialise the plot
fig = plt.figure()
ax1 = plt.subplot(1, 1, 1)

# Coordinates of the robot
xs = []
ys = []

# Coordinates and text of the Object
xt = []
yt = []
tt = []

def callback(data):
    """
    Function that is called every time the data is obtained
    data - The message that is obtained from the topic that this
           node is subscribed to
    """
    xs.append(data.x)
    ys.append(data.y)

def listener():
    """
    Function that calls the callback function and initializes this node
    """
    rospy.init_node('plot', anonymous=True)
    # Subscribe to the odometry raw data
    rospy.Subscriber('/odometry_raw', Vector3, callback)
    rospy.spin()

def animate(i):
    """
    i is the interval
    """ 
    ax1.clear()
    font_dict = {'family':'sans-serif',
                 'color':'darkred',
                 'size':8}
    for i in range(len(xt)):
        ax1.text(xt[i], yt[i], tt[i], fontdict=font_dict)
    ax1.plot(xs, ys)
    #ax1.scatter(xt, yt, 'yo')

    # This is for plotting the coordinates and the class of the detected object
    animated_plot = plt.plot(xt, yt, 'yo')[0]
    animated_plot.set_xdata(xt)
    animated_plot.set_ydata(yt)
    plt.draw()

# 'Spin' the animation
ani = anim.FuncAnimation(fig, animate, interval=1000)
plt.show()

# Call the robot listener
listener()