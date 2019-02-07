import serial
import time
import datetime
import subprocess
#sudo chmod 777 /dev/ttyUSB0

rhino_serial = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)    
rhino_serial1 = serial.Serial('/dev/ttyUSB1',9600,timeout=0.5)    

rhino_serial1.flushOutput()
rhino_serial1.flushInput()
rhino_serial.flushOutput()
rhino_serial.flushInput()
"""
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout
"""
from multiprocessing import Process
import sys

rocket = 0
'''
def func1():
    global rocket
    print 'start func1'
    while rocket < sys.maxint:
        rocket += 1
    print 'end func1'

def func2():
    global rocket
    print 'start func2'
    while rocket < sys.maxint:
        rocket += 1
    print 'end func2'

'''

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

time.sleep(5)
print "Ready"
input_data = 'Y'
input_data1 = 'Y' 
Rhino_send1(input_data1)
Rhino_send(input_data)
input_data = 'm150'
input_data1 = 'm150' 
Rhino_send1(input_data1)
Rhino_send(input_data)
while True:
#    w = raw_input("r/w:")
#    k = raw_input("Port:")
#    input_data = raw_input("Enter:")
    m = raw_input("Hi:")
    if(m=='f'):
       input_data = 's-150'
       input_data1 = 's150'
    elif(m=='m'):
       input_data = 'p0'
       input_data1 = 'p0'
    elif(m=='s'):
       input_data = 's0'
       input_data1 = 's0'
    elif(m=='l'):
       input_data = 's150'
       input_data1 = 's150'
    elif(m=='r'):
       input_data = 's-150'
       input_data1 = 's-150'
    elif(m=='b'):
       input_data = 's150'
       input_data1 = 's-150'
    p1 = Process(target = Rhino_send1(input_data1))
    
    p2 = Process(target = Rhino_send(input_data))
    p2.start()
    p1.start()

#    subprocess_cmd('echo a; echo b')
#    Rhino_send1(input_data1)
#    Rhino_send(input_data)
    
#cable WHITE to Orange
#cable green to yellow
