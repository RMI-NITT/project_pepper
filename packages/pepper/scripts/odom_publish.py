#!/usr/bin/env python

"""Script to publish odometry data"""
import serial
import math
import time

def motor_serial_write(motor_serial, command):
    """Method to write the command to the motors

    :param motor_serial The serial port to write to
    :param command The command to issue to the motor
    """
    # P - Read write encoder position in Rhino Motor RMCS220x series
    motor_serial.write(command + "\n\r")
    time.sleep(0.05)
    motor_serial.flushInput()
    motor_serial.flushOutput()


def motor_serial_read(motor_serial):
    """Method to read the data from the encoders

    :param motor_serial The serial port to read from
    """
    # This does something!
    motor_serial.write('P\n\r')
    time.sleep(0.1)
    count = motor_serial.readline()
    motor_serial.flushInput()
    motor_serial.flushOutput()

    # Check if the input string is garbage
    # If NOT garbage, convert to int and return count
    ticks = ''
    for i in count:
        if i.isdigit() or i == '-':
            ticks = ticks + i
    if ticks != '':
        return int(ticks)
    else:
        return -1


def main():

    # Subject to change
    motor_left = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    motor_right = serial.Serial("/dev/ttyUSB1", 9600, timeout=0.5)

    motor_left.flushOutput()
    motor_right.flushOutput()
    motor_left.flushInput()
    motor_right.flushInput()

    time.sleep(1)
    print "Ready!"

    # Initialize the motors to 0 encoder value
    motor_serial_write(motor_left, "P0")
    motor_serial_write(motor_right, "P0")

    # M200 sets the max speed of the motor to 200
    motor_serial_write(motor_left, "M200")
    motor_serial_write(motor_right, "M200")

    # R900 does a half rotation
    motor_serial_write(motor_left, "S100")
    motor_serial_write(motor_right, "S100")

    print "Setup motor"
    
    while True:

        try:
            lt = motor_serial_read(motor_left)
            rt = motor_serial_read(motor_right) 

            print lt, rt

        except KeyboardInterrupt:
            motor_serial_write(motor_left, "S0")
            motor_serial_write(motor_right, "S0")
            print "Stopping both motors!!"
            break



if __name__ == "__main__":
    main()