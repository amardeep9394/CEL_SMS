#!/usr/bin/python
import MySQLdb
# insert the new system into system information table
class insert_system_detail():
	# Open database connection
	def __init__(self):
		self.db = MySQLdb.connect('localhost','root','cel123','remote_monitor_v1')
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor()
	
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
	# function to insert data into system_information table 
	def sql_query_to_insert(self,data_lst):
		import time
		
		sql_query = """USE remote_monitor_v1"""
		self.execute_query(sql_query)
		#date form is yyyy-mm-dd and time is hh:mm:ss

		sys_id = data_lst[0]
		region = data_lst[1]
		division = data_lst[2]
		sys_type = data_lst[3]
		stn_name = data_lst[4]
		mob_no = data_lst[5]

		if sys_type == "MSDAC":
			no_of_dp = data_lst[7]
			no_of_ts = data_lst[6]
		else:
			no_of_dp = ""
			no_of_ts = ""
		date = time.strftime("%Y-%m-%d")
		time = time.strftime("%H:%M:%S")

		
		try:	
			sql = "INSERT INTO System_Information(Region, Division, System_Type, Station_Name, System_ID, Mobile_number, No_of_DP, No_of_TS, Date,Time,System_Status) VALUES ('"+region+"', '"+division+"','"+sys_type+"','"+stn_name+"', '"+sys_id+"','"+mob_no+"', '"+no_of_dp+"','"+no_of_ts+"','"+date+"','"+time+"','"+''+"')"

		
			self.execute_query(sql)
		
		except:
			raise ValueError


