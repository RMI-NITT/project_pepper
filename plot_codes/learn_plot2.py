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

ser = serial.Serial('/dev/ttyACM0', 9600)

def read_data():
    try:
        line = ser.readline()
        data = [int(val) for val in line.split(' ')]
        if len(data) == 2:
            xs.append(data[0])
            ys.append(data[1])
    except Exception as e:
        print e.message
        print "Exiting"


def animate(i):
    """
    i is the interval
    """ 
    read_data()
    ax1.clear()
    ax1.plot(xs, ys)

ani = anim.FuncAnimation(fig, animate, interval=1000)
plt.show()