"""
Code to detect keyboard interrupts and print the requisite velocities to the terminal
"""
import serial
import time
import datetime
import subprocess
from pynput import keyboard

rhino_serial = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)    
rhino_serial1 = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5) 

rhino_serial1.flushOutput()
rhino_serial1.flushInput()
rhino_serial.flushOutput()
rhino_serial.flushInput()
def Rhino_send(s):
    global rhino_serial
    rhino_serial.write(s+'\n\r')
    #time.sleep(0.2)
    rhino_serial.flushInput()
    rhino_serial.flushOutput()

def Rhino_read(r):
    global rhino_serial
    rhino_serial.write(r +'\n\r')
    time.sleep(0.2)
    read = rhino_serial.readline()
    rhino_serial.flushInput()
    rhino_serial.flushOutput()
    a = ''
    for i in read:
        if i.isdigit() or i=='-':
            a=a+i
    if a!='':
        return int(a)
    else:
        return 0

def Rhino_send1(s):
    global rhino_serial1
    rhino_serial1.write(s+'\n\r')
    #time.sleep(0.2)
    rhino_serial1.flushInput()
    rhino_serial1.flushOutput()

def Rhino_read1(r):
    global rhino_serial1
    rhino_serial1.write(r +'\n\r')
    time.sleep(0.2)
    read = rhino_serial1.readline()
    rhino_serial1.flushInput()
    rhino_serial1.flushOutput()
    a = ''
    for i in read:
        if i.isdigit() or i=='-':
            a=a+i
    if a!='':
        return int(a)
    else:
        return 0


print "Press up for forward\nPress down for reverse\nPress left for left\nPress right for right\n" \
+ "Press s for stop\nPress escape to exit\n"
Rhino_send1('Y')
Rhino_send('Y')
ls = 0
rs = 0

def on_press(key):
    global ls, rs
    try:
        a = key.char
        if a == 's':
            ls = 0
            rs = 0
	 
	Rhino_send1('s'+str(ls))
	Rhino_send('s'+str(rs))
        print ls, rs
    except AttributeError:
        if key == keyboard.Key.up:
            if ls < 250:
                ls += 5
            if ls < 0:
                ls = 0
            if rs > -250:
                rs -= 5
            if rs > 0:
                rs = 0
        elif key == keyboard.Key.down:
            if ls > -250:
                ls -= 5
            if ls > 0:
                ls = 0
            if rs < 250:
                rs += 5
            if rs < 0:
                rs = 0
        elif key == keyboard.Key.right:
            if ls > -250:
                ls -= 5
            if ls > 0:
                ls = 0
            if rs > -250:
                rs -= 5
            if rs > 0:
                rs = 0
        elif key == keyboard.Key.left:
            if rs < 250:
                rs += 5
            if rs < 0:
                rs = 0
            if ls < 250:
                ls += 5
            if ls < 0:
                ls = 0
        
	Rhino_send1('s'+str(ls))
	Rhino_send('s'+str(rs))
        print ls, rs

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False



# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
