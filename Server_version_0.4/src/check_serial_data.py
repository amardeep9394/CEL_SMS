#!/usr/bin/python
import serial
import time, datetime
import re
import sys
import MySQLdb
from insert_sms_data import sms_process
class Process_serial_data():
    def __init__(self):
        self.db = MySQLdb.connect('localhost','root','cel123','remote_monitor_v1')
	# prepare a cursor object using cursor() method
	self.cursor = self.db.cursor()
	self.create_table()
    def execute_query(self,sql):
		try:
			# Execute the SQL command
			
			self.cursor.execute(sql)

			# Commit your changes in the database
			self.db.commit()
			return "Success"
		except:
			# Rollback in case there is any error
			self.db.rollback()		
			return "Failed"

    # create table of inside database
    def create_table(self):

	    # use database
	    sql_query = """USE remote_monitor_v1"""
	    self.execute_query(sql_query)

	    # create table for Username Infomration
	    sql_query = """CREATE TABLE IF NOT EXISTS serial_data (
                                id bigint(20) NOT NULL AUTO_INCREMENT,
				System_ID varchar(20) NOT NULL, 
				message text NOT NULL,
				Date Date NOT NULL,
				Time Time NOT NULL,
				Flag tinyint(1) NOT NULL Default 0,
				PRIMARY KEY (id)
				)"""

	    self.execute_query(sql_query)
	    self.read_serial_data()
	
    
    def read_serial_data(self):
        z1baudrate = 9600
        z1port = '/dev/ttyUSB0'  # set the correct port before run it
        z1serial = serial.Serial(port=z1port, baudrate = z1baudrate)
        z1serial.timeout = 2  # set read timeout
        # print z1serial  # debug serial.
        print z1serial.is_open  # True for opened
        if z1serial.is_open:
            #pkt = ''
            while True:
                try:
                    msg = z1serial.inWaiting()
                    #print msg   
                    if msg:
                        data = z1serial.readline(msg)
                        #print data
                        data = re.sub(r'\s+','',data)
                        data = data[data.find('%')+1 : data.find('$')]
                        if data.isalnum():
                            
                            data = '%'+data+'$'
                            #print data
                            self.insert_serial_data(data)
                            #print data,len(data),type(data),data[-1]
                        else:
                            pass
                        
                    else:
                        print 'no data'
                    #time.sleep(1)
                except:
                    pass
        else:
            print 'z1serial not open'

    def insert_serial_data(self,line):
        now = datetime.datetime.now()
        #sysid = 'EM08C1'
        date = now.strftime("%Y-%m-%d")
	time = now.strftime("%H:%M:%S")
	try: 
            print line
            if line[2] == '1':
                sysid = 'MSDAC_Card1'
            if line[2] == '2':
                sysid = 'MSDAC_Card2'
            if line[2] == '3':
                sysid = 'MSDAC_Card3'
            if line[2] == '4':
                sysid = 'MSDAC_Card4'
            if line[2] == '5':
                sysid = 'MSDAC_Card5'
                
            #for T packet
            if line[0:2] == '%T'and line[-1] == '$' and len(line) == 15:
                sql_query = "insert into serial_data(System_ID, message, Date, Time) values ('"+sysid+"','"+line+"','"+date+"','"+time+"')"		
                self.execute_query(sql_query)
                print 'pkt T inserted successfully'
            #for D packet
            #print 'D',len(line), line[-1]
            if line[0:2] == '%D' and line[-1] == '$' and len(line) == 18 :
                sql_query = "insert into serial_data(System_ID, message, Date, Time) values ('"+sysid+"','"+line+"','"+date+"','"+time+"')"		
                self.execute_query(sql_query)
                print 'pkt D inserted successfully'
            sql = "select * from serial_data where Flag = 0"
	    self.execute_query(sql)
	    
	    sms=self.cursor.fetchall()
	    
	    for i in range(0,len(sms)):
                        
                    d = sms_process()
                    d.break_serial_data(sms[i][1],sms[i][2],sms[i][3],sms[i][4])
                    id_no = sms[i][0]
		    sql_query = "update serial_data set Flag = '1' where id = '"+str(id_no)+"'"

                    self.execute_query(sql_query)
                    
        except:
            pass

run = Process_serial_data()
