#!/usr/bin/python2
import MySQLdb
from insert_sms_data import sms_process
import os

#to find the path to access the data json file
ab= os.path.dirname(os.getcwd())+'/data'

class read_sms():
	# Open database connection
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
		sql_query = """CREATE TABLE IF NOT EXISTS sms_data (
				id bigint(20) NOT NULL Primary Key, 
				phone_number varchar(12) NOT NULL, 
				message text NOT NULL,
				dt datetime NOT NULL,
				isnew tinyint(1) NOT NULL,
				processed tinyint(1) NOT NULL Default 0
				)"""

		self.execute_query(sql_query)
		self.insert_sms()
	# insert sms from data.json file into the database
	def insert_sms(self):
		# open data.json file
                sms_data1 = eval(open(ab+"/data.json").read())
		no_of_sms = len(sms_data1["messages"])

		for i in range(0,no_of_sms):
			id_no = sms_data1["messages"][i]['id']
			phone_no = sms_data1["messages"][i]['number']
			msg = sms_data1["messages"][i]['message'].replace('\/','/')
			dt = sms_data1["messages"][i]['date']
			isnew = sms_data1["messages"][i]['isNew']
			if '%T' in msg or'%D' in msg:

				sql_query = "insert into sms_data(id, phone_number, message, dt, isnew) values ('"+id_no+"','"+str(phone_no)+"','"+msg+"','"+dt+"','"+str(isnew)+"')"		

				self.execute_query(sql_query)
				
		print "Inserted Successfully"

		

	

x=read_sms()

