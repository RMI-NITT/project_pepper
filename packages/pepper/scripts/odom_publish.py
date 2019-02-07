#!/usr/bin/env python

"""Script to publish odometry data"""
import serial
import math
import time

import rospy
import roslib


def serial_write(motor_serial, command):
    """Method to write the command to the motors

    :param motor_serial The serial port to write to
    :param command The command to issue to the motor
    """
    # P - Read write encoder position in Rhino Motor RMCS220x series
    motor_serial.write(command + "\n\r")
    time.sleep(0.05)
    motor_serial.flushInput()
    motor_serial.flushOutput()


def serial_read(motor_serial):
    """Method to read the data from the encoders

    :param motor_serial The serial port to read from
    """
    # This does something!
    motor_serial.write('P\n\r')
    time.sleep(0.05)
    count = motor_serial.readLine()
    motor_serial.flushInput()
    motor_serial.flushOutput()

    # Check if the input string is garbage
    # If NOT garbage, convert to int and return count
    ticks = ""
    for i in count:
        if i.isdigit() or i == "-":
            ticks += i
        if ticks != "":
            return int(ticks)
        else:
            return 0


def main():
    # Subject to change
    motor_left = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    motor_right = serial.Serial("/dev/ttyUSB1", 9600, timeout=0.5)

    motor_left.flushOutput()
    motor_right.flushOutput()

    motor_left.flushInput()
    motor_right.flushInput()

    # Initialize the motors to 0 encoder value
    serial_write(motor_left, "P0")
    serial_write(motor_right, "P0")

    rospy.init_node("odom_publisher", anonymous=True)
    encoder_publisher = rospy.Publisher("odom", Encoders, queue_size=10)
    rate = rospy.Rate(50)

    prev_time = None
    cur_time = None

    while not rospy.is_shutdown():
        try:
            left_ticks = serial_read(motor_left)
            left_ticks = left_ticks * -1

            right_ticks = serial_read(motor_right)

            print left_ticks, right_ticks

        # when ctrl+c is pressed
        except rospy.ROSInterruptException:
            print rospy.ROSInterruptException
            pass


if __name__ == "__main__":
    main()
