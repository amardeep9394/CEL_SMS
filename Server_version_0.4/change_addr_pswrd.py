#!/usr/bin/python2

from os import listdir

# Change IP address at all instance of templates
for filename in listdir("./template"):
	
	with open('./template/' + filename) as f:
		newText=f.read().replace('192.168.1.230','127.0.0.1')
	with open('./template/' + filename,"w") as f:
		f.write(newText)

# Change IP address and database password at all instance of source file
for filename in listdir("./src"):

	# Change IP address at all instance of source file
	with open('./src/' + filename) as f:
		newText=f.read().replace('192.168.1.230','127.0.0.1')
	with open('./src/' + filename,"w") as f:
		f.write(newText)

	# Change database password at all instance of source file
	with open('./src/' + filename) as f:
		newText=f.read().replace('masamb123', 'cel123')
	with open('./src/' + filename,"w") as f:
		f.write(newText)
			
