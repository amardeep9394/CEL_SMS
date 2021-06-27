#!/usr/bin/python

import StringIO
import pycurl
import json
import time
import os
import pyinotify

import sys
import glob
import serial
import threading
from serial import Serial
from serial.tools import list_ports

#to find the path to access the data json file
ab= os.path.dirname(os.getcwd())+'/data'

serPortObj=[]

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'): # Windows
        ports = ['COM%s' % (i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'): # Linux
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#-----End of 'serial_ports' Function--------------
portList = list(serial_ports())
portList.sort()

print portList




class SerialData(object):
	#It is wx.Panel class which consist algorithm for extracting data from file and serial port
	def __init__(self,portName):
		print portName
		self.lines=[]
		self.portName=portName
		self.serial_port_connect(self.portName)
	#-----End of '__init__' Function--------------

	def serial_port_connect(self, portName):
		#Method is used to connect the port from were data will received.
		# Configure the serial connections
		# this is set up to start with; 
		self.ser = serial.Serial(
		    port = portName,
		    baudrate=9600,
		    parity=serial.PARITY_NONE,
		    stopbits=serial.STOPBITS_ONE,
		    bytesize=serial.EIGHTBITS,
		    timeout = 0
		)
		serPortObj.append(self.ser)
		# Check for open Serial port
		if self.ser.isOpen():
		    # Show that port is open and that you are connected
		    print 'Connected to '+str(len(serPortObj))+': '+portName+'\n'
		# Create and start Serial port receiving thread as daemon
		# for auto stop and cleanup
		self.thread = threading.Thread(target=self.receiving, args=(self.ser,))
		self.thread.setDaemon(True)
		self.thread.start()
	#-----End of 'serial_port_connect' Function--------------

	def receiving(self, ser):
		#Method used to receive data from port now will be handling.
		# Serial port receiving, ran under thread
		count=0;
		while True:
			# Small delay for CPU savings
			##time.sleep(0.001)
			try:
				if ser.inWaiting() >0:
					msg = ser.readline()
					print msg
					# change data in msdState
					with open(ab+'/msdState.json','w') as f:
						f.write(msg)
			except:
				pass
	#-----End of 'receiving' Function--------------
#used to perform connection and watching the updation in the file
class MyEventHandler(pyinotify.ProcessEvent):
	#establish the connection with server and always watch that the updation in file if any the data is send to server
	def process_IN_MODIFY(self, event):

		print "MODIFY event:","--", event.pathname
		#******** put client code here************
		url = 'http://127.0.0.1:8080/hello'

		c = pycurl.Curl()

		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.POST, 1)
		#c.setopt(c.CONNECTTIMEOUT, 5)
		#c.setopt(c.TIMEOUT, 8)
		#c.setopt(c.PROXY, 'http://192.168.1.131:8080/hello')

		# loading json file to post

		# posting data to server

		# username and password for authentication
		c.setopt(pycurl.USERPWD, "%s:%s" % (str('abhi'), str('masamb')))

		# header information

		fout = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, fout.write)

		c.perform()

		http_code = c.getinfo(pycurl.RESPONSE_CODE)
		response_data = fout.getvalue()
		print "http_code---> ",http_code
		print "response_data---> ",response_data

		if http_code is 200 and response_data == 'AUTHORISED USER':
			print "RRRRUNNNNNNNNNNNNNNNNNNNNNNNNN"
			# open file to read the input data
			'''f = open(ab+'/msdState.json','r')
			sms = f.read()'''

                        # open data.json file
                        sms_data1 = eval(open("/Desktop/data.json").read())
                        raw_data1 = sms_data1["messages"][-1]["message"].split(',')
                        raw_data2 = sms_data1["messages"][-1]["date"].split(" ")

                        sms = raw_data1[0]+','+raw_data2[0].replace("-","/")+','+raw_data2[1]+','+raw_data1[-1]

			# Process SMS to verify data
			sms_data = sms.split(",")
			print "sms_data",sms_data
			#check that the data contains information in form of sms or json_file
			#if '+91' in sms:
			if len(sms_data) == 4: 
				if len(sms_data[0]) == 13 and len(sms_data[1]) == 10 and len(sms_data[2]) == 8:
					url = url+'/msdacsms'
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.POST, 1)

					# posting data to server
					c.setopt(pycurl.POSTFIELDS, str(sms))
					c.setopt(pycurl.VERBOSE, 1)

					# header information
					c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','STATION: GAMBIRI ROAD'])
		
					c.perform()
					c.close()
				else:	
					print "DATA IS INVALID"
					pass
					
			else:
				print "INSUFFICIENT DATA"
				pass
		else:
			print response_data

		






if __name__ == '__main__':


    	# watch manager
	wm = pyinotify.WatchManager()
	wm.add_watch('/Desktop/data.json', pyinotify.ALL_EVENTS, rec=True)

	# notifier
	notifier = pyinotify.Notifier(wm, MyEventHandler())
	notifier.loop()
	# server address
