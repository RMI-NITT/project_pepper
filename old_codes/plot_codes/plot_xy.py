"""
Code to plot the real time data to the system
"""
import serial
import numpy as np
from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    # Set up the animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 150), ylim=(0, 150))
    a0 = plt.plot([], [])
    a1 = plt.plot([], [])
