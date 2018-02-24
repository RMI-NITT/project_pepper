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

if __name__ == "__main__":
	Rhino_send('Y')
	Rhino_send1('Y')
	time.sleep(2)
	print "Done tuning"
	Rhino_send('p0')
	Rhino_send1('p0')
	in0 = "s-"
	in1 = "s"
	in0_data = 150
	in1_data = 150 
	out0 = 0
	out1 = 0		
	for i in range(10):
		Rhino_send(in0+str(in0_data))
		Rhino_send1(in1+str(in1_data))				
		#out0_prev = out0
		#out1_prev = out1
		#out0 = Rhino_read('p')
		#out1 = Rhino_read1('p')
		#print "0", out0_prev - out0
		#print "1", out1_prev - out1
		'''
		print Rhino_read('A'), Rhino_read('B'), Rhino_read('C')
		print Rhino_read1('A'), Rhino_read1('B'), Rhino_read1('C')
		'''
	Rhino_send('s0')
	Rhino_send1('s0')
	
