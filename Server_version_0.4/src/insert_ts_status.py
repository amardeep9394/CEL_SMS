#!/usr/bin/python

import MySQLdb
from Database_Operation import Db_Operation
# class to perform the opeartion in database like checking of system ID exits or not in the database and perform various operations as insertion, deletion etc.
class Db_process():
	# Open database connection
	def __init__(self,data):
		self.db = MySQLdb.connect('localhost','root','cel123','remote_monitor_v1')
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor()
	
		# object of Database_Operation
		self.db_op = Db_Operation()

		fetch_data = self.check_system_ID(data)	
		if fetch_data != "Failed" and fetch_data != 0:
			data["Region"] = fetch_data[0]
			data["Division"] = fetch_data[1]
			data["System_Type"] = fetch_data[2]
			self.check_loop(data)
			
		
		
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
	# function to check system id is exist already exist in database or not
	def check_system_ID(self,data):

		condition = "WHERE System_ID = "+'"'+data["System_ID"]+'"'
					
		lst_Operation = ["SELECT","System_Information",["*"],[condition],data]

		# It return some value if data exist
		check = self.db_op.process_request(lst_Operation)
		

		# check the response from database
		if len(check) == 1:
			lst_Operation = [check[0][0],check[0][1],check[0][2]]

			return lst_Operation
		else:
			return "Failed"

		
	# get all data to pass into the database
	def get_all_data(self,lst_Operation):
		# If data is in the form of dictionary then convert it into list
		opn = eval(open('column.py').read())
		opn = opn[lst_Operation[1]]
		
		lst_of_data = []
		# store element in a list based on there keys from dictionary
		for ele in opn:
			if ele in lst_Operation[-1]:
				lst_of_data.append(lst_Operation[-1][ele])
			else:
				lst_of_data.append("")

		lst_Operation[-1] = lst_of_data

		return lst_Operation

	# Insert data into History_Information table
	def insert_into_history(self,lst_of_data):

		lst_Operation = ["INSERT","History_Information",[],[],lst_of_data]
		
		# get the data in list
		lst_Operation = self.get_all_data(lst_Operation)

		# Pass data to insert into History_Information table
		insert = self.db_op.process_request(lst_Operation)
		


		return

	# one by one each ts_id is checking and on the basis of existance in database it will insert or update
	def check_loop(self,lst_of_data):

		card_no = [str(i) for i in range(1,6)]
		ts_no = [str(j) for j in range(8)]
		for k in card_no:
			for t in ts_no:
				if lst_of_data[k+t] == "NULL":
					pass
				else: 
					tsid = k+t
					sysid = lst_of_data["System_ID"]
					ts_sts = lst_of_data[k+t]
					date = lst_of_data["Date"]
					time = lst_of_data["Time"]
					check = self.check_ts_id(tsid,sysid)

					if len(check) == 0:

						sql = "INSERT INTO TS_Status(TS_ID,System_ID,TS_Status,Date,Time) VALUES ('"+tsid+"','"+sysid+"','"+ts_sts+"','"+date+"','"+time+"')"
						self.execute_query(sql)
						self.check_System_Status(lst_of_data)
						
						#data for history
						history_data = {}
						history_data["System_ID"] = sysid
						history_data["Station_Name"] = lst_of_data["Station_Name"]
						history_data["Date"] = date
						history_data["Time"] = time
						history_data["Region"] = lst_of_data["Region"]
						history_data["Division"] = lst_of_data["Division"]
						history_data["TS_ID"] = tsid
						history_data["TS_Status"] = ts_sts
						history_data["System_Type"] = lst_of_data["System_Type"]
						history_data["System_Status"] = lst_of_data["System_Status"]
						history_data["TS_Info"] = lst_of_data["Updated_TS_Info"]

						self.insert_into_history(history_data)
					else:
						if check[0][2] != ts_sts: 

							sql = "UPDATE TS_Status SET TS_Status = '"+ts_sts+"', Date = '"+date+"', Time = '"+time+"' WHERE TS_ID = '"+tsid+"'AND System_ID = '"+sysid+"'"
							self.execute_query(sql)
							self.check_System_Status(lst_of_data)
							#data for history
							history_data = {}
							history_data["System_ID"] = sysid
							history_data["Station_Name"] = lst_of_data["Station_Name"]
							history_data["Date"] = date
							history_data["Time"] = time
							history_data["Region"] = lst_of_data["Region"]
							history_data["Division"] = lst_of_data["Division"]
							history_data["TS_ID"] = tsid
							history_data["TS_Status"] = ts_sts
							history_data["System_Type"] = lst_of_data["System_Type"]
							history_data["System_Status"] = lst_of_data["System_Status"]
							history_data["TS_Info"] = lst_of_data["Updated_TS_Info"]
					
							self.insert_into_history(history_data)
						else:
							pass
					

	# checking of the track section id from ts status
	def check_ts_id(self,tsid,sysid):
		sql = "SELECT * FROM TS_Status WHERE TS_ID = '"+tsid+"' AND System_ID = '"+sysid+"'"
		self.cursor.execute(sql)
		d = self.cursor.fetchall()
		return d
	# Update the system status in syatem information and system status table
	def check_System_Status(self,lst_of_data):

		lst_key = []
		keys_str = []
		
		check = 'ERROR' in lst_of_data.values()
		if check == True:
			lst_of_data["System_Status"]='Unknown'
			for key, value in lst_of_data.items():
				if value == 'ERROR':
					lst_key.append((key,value)) #it stores key and value as a tuple in list which have error in track section
					keys_str.append(key)
		
		else:
			lst_of_data["System_Status"]='OK'
			keys_str.append('OK')


		ts_id = {}
		count = 0
		disp = []

		card_no = [str(i) for i in range(1,6)]
		ts_no = [str(j) for j in range(8)]
		ts_name = [str(st)+'T' for st in range(1,41)]

		for k in card_no:
			for t in ts_no:
				ts_id[k+t] = ts_name[count]
				count += 1


		for i,key in enumerate(keys_str):
			

			if key == "OK":
				disp.append("OK")
			else:
				disp.append(ts_id[key]+"-"+lst_key[i][1][:1])
		

		lst_of_data["Updated_TS_Info"]= ','.join(disp)

		sysid = lst_of_data["System_ID"]		
		sys_sts = lst_of_data["System_Status"]
		ts_info = lst_of_data["Updated_TS_Info"]
		date = lst_of_data["Date"]
		time = lst_of_data["Time"]
		region = lst_of_data["Region"]
		div = lst_of_data["Division"]
		sys_type = lst_of_data["System_Type"]

		sql = "select * from  System_Status WHERE System_ID = '"+sysid+"'"
		self.cursor.execute(sql)
		d = self.cursor.fetchall()
		if len(d) == 1:
		
			sql = "UPDATE System_Status SET System_Status = '"+sys_sts+"', Updated_TS_Info = '"+ts_info+"', Date = '"+date+"', Time = '"+time+"' WHERE System_ID = '"+sysid+"'"
		
			self.execute_query(sql)
		else:
			sql = "INSERT INTO System_Status(Region, Division, System_Type, System_ID, System_Status, Date,Time,Updated_TS_Info) VALUES ('"+region+"', '"+div+"', '"+sys_type+"', '"+sysid+"', '"+sys_sts+"','"+date+"','"+time+"', '"+ts_info+"')"
			self.execute_query(sql)

		sql = "UPDATE System_Information SET System_Status = '"+sys_sts+"', Date = '"+date+"', Time = '"+time+"' WHERE System_ID = '"+sysid+"'"
		self.execute_query(sql)
		
	






