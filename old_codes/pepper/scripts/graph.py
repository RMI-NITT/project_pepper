#!/usr/bin/env python
import geometry_msgs.msg
import rospy
from geometry_msgs.msg import Vector3
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style
import time
from depth.msg import cood
import math
# Basic style of the plot
style.use('fivethirtyeight')

# Initialise the plot
fig = plt.figure()
ax1 = plt.subplot(1, 1, 1)

# Coordinates of the robot
xs = []
ys = []
curr_thet = 0
xs.append(0.0)
ys.append(0.0)


# Coordinates and text of the Object
xt = []
yt = []
tt = []
plotted = dict()

def callback(data):
    xs.append(data.x)
    ys.append(data.y)
    curr_thet = data.z
    #print(data.x,data.y)

def check(x_o, y_o, c_o, dic):
    thresh = 0.5
    global plotted
    #print 'before for in check'
    if(len(xt)==0):
        #print "in 1st if"
        dic[c_o] = [1,True]
        plotted[c_o] = True
        return
    for i in range(len(xt)):
        #print ('inside for in check')
        if tt[i] == c_o and plotted.get(c_o, False):
            di = math.sqrt((xt[i]-x_o)**2 + (yt[i] - y_o)**2)
            #print '1'
            if di < thresh:
                dic[c_o] = [dic.get(c_o, [])[0], False]
                #print '2'
        elif not plotted.get(c_o, False):
            dic[c_o] = [1, True]
            plotted[c_o] = True            

def object_callback(data):
    global plotted
    r_list = data.x
    thet_list = data.y
    num = data.n
    cls_list = data.c
    dic = dict()
    for i in range(num):
        if len(dic.get(cls_list[i],[]))==0:
            dic[cls_list[i]] = [1,True]
        else:    
            dic[cls_list[i]] = [dic.get(cls_list[i], [])[0]+1, False]
        #print 'in 1st for'
    for i in range(num):
        r = r_list[i]
        t = thet_list[i]
        x_o = xs[-1] + r*math.cos(curr_thet + t)
        y_o = ys[-1] + r*math.sin(curr_thet + t)
        c_o = cls_list[i]
        #print 'in 2nd for'
        print x_o,y_o,c_o
        check(x_o, y_o, c_o, dic)
        
    for i in range(num):
        r = r_list[i]
        t = thet_list[i]
        x_o = xs[-1] + r*math.cos(curr_thet + t)
        y_o = ys[-1] + r*math.sin(curr_thet + t)
        c_o = cls_list[i]
        #print 'in 3rd for'

        no, bo = dic.get(cls_list[i], [])
        if bo == True:
            xt.append(x_o)
            yt.append(y_o)
            tt.append(c_o)

def listener():

    rospy.init_node('graph', anonymous=True)
    data = rospy.Subscriber("/coord_converter",cood, object_callback)

    rospy.Subscriber('/odometry_raw', Vector3, callback)
#    rospy.spin()
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

if __name__ == '__main__':
    ani = anim.FuncAnimation(fig, animate)
    listener()
    plt.show()
