"""
Script to plot data real time in the arduino
"""
import serial

import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style

import time

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = plt.subplot(1, 1, 1)

xs = []
ys = []

xt = []
yt = []
tt = []

ser = serial.Serial('/dev/ttyACM0', 9600)

def read_data():
    try:
        line = ser.readline()
        # data = [int(val) for val in line.split(' ')]
        data = line.strip().split(' ')
        print data
        if len(data) == 2:
            data = [int(val) for val in data]
            xs.append(data[0])
            ys.append(data[1])
        elif len(data) == 3:
            xt.append(int(data[0]))
            yt.append(int(data[1]))
            tt.append(data[2])

    except Exception as e:
        print e.message
        print "Exiting"


def animate(i):
    """
    i is the interval
    """ 
    read_data()
    ax1.clear()
    font_dict = {'family':'sans-serif',
                 'color':'darkred',
                 'size':8}
    for i in range(len(xt)):
        ax1.text(xt[i], yt[i], tt[i], fontdict=font_dict)
    ax1.plot(xs, ys)
    #ax1.scatter(xt, yt, 'yo')

    animated_plot = plt.plot(xt, yt, 'yo')[0]
    animated_plot.set_xdata(xt)
    animated_plot.set_ydata(yt)
    plt.draw()

ani = anim.FuncAnimation(fig, animate, interval=1000)
plt.show()