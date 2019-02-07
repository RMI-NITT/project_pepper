import serial
import time
import datetime

rhino_serial = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)    
rhino_serial1 = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5)    

rhino_serial1.flushOutput()
rhino_serial1.flushInput()
rhino_serial.flushOutput()
rhino_serial.flushInput()

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

def Rhino_send1(s):
    global rhino_serial1
    rhino_serial1.write(s+'\n\r')
    time.sleep(0.2)
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

time.sleep(5)
print "Ready"
while True:
    w = raw_input("r/w:")
    k = raw_input("Port:")
    input_data = raw_input("Enter:")
    if(w=='w'):
     if(k=='1'):
       Rhino_send1(input_data)
     elif(k=='0'):
       Rhino_send(input_data)
    elif(w=='r'):
     if(k=='1'):
       print Rhino_read1(input_data)
     elif(k=='0'):
       print Rhino_read(input_data)

#cable WHITE to Orange
#cable green to yellow
