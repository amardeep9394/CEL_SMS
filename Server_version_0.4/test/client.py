#!/usr/bin/python

import StringIO
import pycurl
import json
import time
import os
#import pyinotify

#class MyEventHandler(pyinotify.ProcessEvent):
	
	#def process_IN_MODIFY(self, event):

		#print "MODIFY event:","--", event.pathname
		#******** put client code here************
#to find the path to access the data json file
ab= os.path.dirname(os.getcwd())+'/data'
#print ab

def main():
	'''# watch manager
	wm = pyinotify.WatchManager()
	wm.add_watch('../prj/cel_gui/dat/msdState.json', pyinotify.ALL_EVENTS, rec=True)

	# event handler
	eh = MyEventHandler()

	# notifier
	notifier = pyinotify.Notifier(wm, eh)
	notifier.loop()'''
	# server address
	url = 'http://192.168.1.231:8080/hello'

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
	#print "http_code---> ",http_code
	#print "response_data---> ",response_data
	
	if http_code is 200 and response_data == 'AUTHORISED USER':
		# open file to read the input data
		f = open(ab+'/msdState.json','r')
		sms = f.read()
		#check that the data contains information in form of sms or json_file
		if '+91' in sms:
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
			url = url+'/msdacdata'
			c = pycurl.Curl()
			c.setopt(pycurl.URL, url)
			c.setopt(pycurl.POST, 1)

			# update date and time
			data_post = eval(open(ab+'/msdState.json').read())
			data_post["Date"] = time.strftime("%Y-%m-%d")
			data_post["Time"] = time.strftime("%H:%M:%S")

			#print data_post
			# loading json file to post
			'''json_file='msdState.json'
			with open('msdState.json') as msdac_json:
				data_post=json.load(msdac_json)'''

			# posting data to server
			c.setopt(pycurl.POSTFIELDS, str(data_post))
			c.setopt(pycurl.VERBOSE, 1)

			# header information
			c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','STATION: GAMBIRI ROAD'])
	
			c.perform()
			c.close()
	else:
		print response_data

	
	
 
if __name__ == '__main__':
    main()
