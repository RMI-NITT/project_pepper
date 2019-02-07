import serial
import time
import datetime

def Rhino_send(s):
    global rhino_serial
    rhino_serial.write(s+'\n\r')
    time.sleep(0.2)
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

time.sleep(5)
print "Ready"
port = raw_input("Port(0/1): ")

rhino_serial = serial.Serial('/dev/ttyUSB' + port, 9600, timeout=0.5)
rhino_serial.flushOutput()
rhino_serial.flushInput()

while True:
    input_data = raw_input("Enter:")
    Rhino_send(input_data)

#cable WHITE to Orange
#cable green to yellow
