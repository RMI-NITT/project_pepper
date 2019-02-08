import serial
import time
import datetime

rhino_serial = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)  
rhino_serial1 = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5)  
rhino_serial.flushOutput()
rhino_serial.flushInput()
rhino_serial1.flushOutput()
rhino_serial1.flushInput()

def Rhino_send(s):
    print s
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
    print s
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
rpm= 200
rpm_1 = 200
time.sleep(5)
val = 1.2
Rhino_send('S200')
Rhino_send1('S200')
print "Ready"
while True:
    tick_old1 = Rhino_read1('P')
    tick_old = Rhino_read('P')
    #w = raw_input("r/w:")
    #k = raw_input("Port:")
    #input_data = raw_input("Enter:")
    #if(w=='w'):
    # if(k=='1'):
    #   Rhino_send1(input_data)
    # elif(k=='0'):
    #   Rhino_send(input_data)
    #elif(w=='r'):
    # if(k=='1'):
    #   print Rhino_read1(input_data)
      
    # elif(k=='0'):
    #   print Rhino_read(input_data)
    #   print Rhino_read('P')
    time.sleep(0.5)
    tick_new1 = Rhino_read1('P')
    tick_new = Rhino_read('P')
    vel_1 = (tick_new1 - tick_old1)*31.4*255/(0.005*2147483648)
    vel = (tick_new - tick_old)*31.4*255/(0.005*2147483648)
    err = val - vel
    err1 = val - vel_1
    rpm = rpm + err*60
    rpm_1 = rpm_1 + err1*60 
    if(abs(err)>0.02):
     Rhino_send('S' + str(int(rpm)))
     #print rpm
    if(abs(err1)>0.02):
     Rhino_send1('S'+ str(int(rpm_1)))
     #print rpm_1 
    
    print '###'
    print vel
    print vel_1
    print '~~~~'
    print err
    print err1
#cable WHITE to Orange
#cable green to yellow
