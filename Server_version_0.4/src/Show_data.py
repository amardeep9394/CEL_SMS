#!/usr/bin/python

import MySQLdb
# used to fecth all the information to display on the server
class Display_data():

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

	# checking the authentication of user
	def check_user(self,data_lst):
		
		if data_lst[2] == 'Admin':
			sql = "select * from User_Credential where Username = '"+data_lst[0]+"' and Password = '"+data_lst[1]+"' and User_type ='"+data_lst[2]+"'"
			
		else:
			sql = "select * from User_Credential where Username = '"+data_lst[0]+"' and Password = '"+data_lst[1]+"' and Region = '"+data_lst[-1]+"'"
			
		self.execute_query(sql)
		check = self.cursor.fetchall()
		return check

	# reterive the information of the all the systems in the form of Dictionary
	def retrieve_data_for_table1(self,Region):
		data = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		if Region == 'Admin':
			sql = "select Count(System_Status) from System_Status where System_Type = 'MSDAC' AND System_Status ='Unknown'"
			self.execute_query(sql)

			msdac_unknown = self.cursor.fetchone()

			sql = "select count(System_Status) from System_Status where System_Type = 'MSDAC' AND System_Status = 'OK' "
			self.execute_query(sql)

			msdac_ok = self.cursor.fetchone()
		
			sql = "select Count(System_Status) from System_Information where System_Type = 'HASSDAC' AND System_Status ='Unknown'"
		
			self.execute_query(sql)

			hassdac_unknown = self.cursor.fetchone()

			sql = "select Count(System_Status) from System_Information where System_Type = 'HASSDAC' AND System_Status  ='OK'"
		
			self.execute_query(sql)

			hassdac_ok = self.cursor.fetchone()
		else:
			sql = "select Count(System_Status) from System_Status where System_Type = 'MSDAC' AND System_Status ='Unknown' and Region = '"+Region+"'"					
		
			self.execute_query(sql)

			msdac_unknown = self.cursor.fetchone()

			sql = "select count(System_Status) from System_Status where System_Type = 'MSDAC' AND System_Status = 'OK' and  Region = '"+Region+"'"
			self.execute_query(sql)

			msdac_ok = self.cursor.fetchone()
		
			sql = "select Count(System_Status) from System_Information where System_Type = 'HASSDAC' AND System_Status ='Unknown' and Region = '"+Region+"'"				
		
			self.execute_query(sql)

			hassdac_unknown = self.cursor.fetchone()

			sql = "select Count(System_Status) from System_Information where System_Type = 'HASSDAC' AND System_Status  ='OK' and Region = '"+Region+"'"				
		
			self.execute_query(sql)

			hassdac_ok = self.cursor.fetchone()
		
		data["MSDAC"]["Total"]=int(msdac_unknown[0]+msdac_ok[0])
		data["MSDAC"]["OK"]=int(msdac_ok[0])
		data["MSDAC"]["Unknown"]=int(msdac_unknown[0])

		data["HASSDAC"]["Total"]=int(hassdac_unknown[0]+hassdac_ok[0])
		data["HASSDAC"]["OK"]=int(hassdac_ok[0])
		data["HASSDAC"]["Unknown"]=int(hassdac_unknown[0])

		data["SSDAC"]["Total"]=0
		data["SSDAC"]["OK"]=0
		data["SSDAC"]["Unknown"]=0


		return data
	# reterive the information from database for the MSDAC
	def retrieve_data_for_table2(self,Region):
		data2 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql = "select System_Information.System_ID,System_Information.Station_Name,System_Status.System_Status, System_Information.No_of_DP, System_Information.No_of_TS, System_Status.Date, System_Status.Time, System_Status.Updated_TS_Info From System_Information JOIN System_Status WHERE System_Information.System_ID = System_Status.System_ID and System_Information.Region = '"+Region+"'"			
		
		self.execute_query(sql)

		d = self.cursor.fetchall()
		
		data2["MSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data2["MSDAC"]["MSDAC ID"] = [x[0] for x in d]
		data2["MSDAC"]["Station Name"] = [x[1] for x in d]
		data2["MSDAC"]["Status"] = [x[2] for x in d]
		data2["MSDAC"]["No. of DP"] = [x[3] for x in d]
		data2["MSDAC"]["No. of TS"] = [x[4] for x in d]
		data2["MSDAC"]["Date"] = [x[5] for x in d]
		data2["MSDAC"]["Time"] = [x[6] for x in d]
		data2["MSDAC"]["Updated_TS_Info"] = [x[7] for x in d]
		
		lst = data2["MSDAC"]["Updated_TS_Info"]
		
		return data2
	# reterive the information from database for the HASSDAC
	def retrieve_data_for_hassdac(self,Region):
		
		data2 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		if Region == 'Admin':
			sql = "SELECT System_Information.System_ID,System_Information.Station_Name,System_Information.System_Status, HASSDAC_System_Status.System1_Status,HASSDAC_System_Status.System2_Status,HASSDAC_System_Status.Date,HASSDAC_System_Status.Time from System_Information JOIN  HASSDAC_System_Status WHERE System_Information.System_ID = HASSDAC_System_Status.System_ID and System_Information.System_Type = 'HASSDAC' "

			self.execute_query(sql)
			d = self.cursor.fetchall()
			data2["HASSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
			data2["HASSDAC"]["HASSDAC ID"] = [x[0] for x in d]
			data2["HASSDAC"]["Station Name"] = [x[1] for x in d]
			data2["HASSDAC"]["Status"] = [x[2] for x in d]
			data2["HASSDAC"]["System1 Status"] = [x[3] for x in d]
			data2["HASSDAC"]["System2 Status"] = [x[4] for x in d]
			data2["HASSDAC"]["Date"] = [x[5] for x in d]
			data2["HASSDAC"]["Time"] = [x[6] for x in d]
			
		else:
			sql = "SELECT System_Information.System_ID,System_Information.Station_Name,System_Information.System_Status, HASSDAC_System_Status.System1_Status,HASSDAC_System_Status.System2_Status,HASSDAC_System_Status.Date,HASSDAC_System_Status.Time from System_Information JOIN  HASSDAC_System_Status WHERE System_Information.System_ID = HASSDAC_System_Status.System_ID and System_Information.Region = '"+Region+"' "

			self.execute_query(sql)
			d = self.cursor.fetchall()

			data2["HASSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
			data2["HASSDAC"]["HASSDAC ID"] = [x[0] for x in d]
			data2["HASSDAC"]["Station Name"] = [x[1] for x in d]
			data2["HASSDAC"]["Status"] = [x[2] for x in d]
			data2["HASSDAC"]["System1 Status"] = [x[3] for x in d]
			data2["HASSDAC"]["System2 Status"] = [x[4] for x in d]
			data2["HASSDAC"]["Date"] = [x[5] for x in d]
			data2["HASSDAC"]["Time"] = [x[6] for x in d]
			
		return data2
	# reterive the information from database for the Track Section
	def retrieve_data_for_table3(self,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql = "select TS_ID,TS_Status,Date,Time,Remarks from TS_Status WHERE System_ID = '"+ID+"'"

		self.execute_query(sql)

		d = self.cursor.fetchall()

		ts_id = {}
		count = 0

		card_no = [str(i) for i in range(1,6)]
		ts_no = [str(j) for j in range(8)]
		ts_name = [str(st)+'T' for st in range(1,41)]

		for k in card_no:
			for t in ts_no:
				ts_id[k+t] = ts_name[count]
				count += 1

		
		data3["MSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data3["MSDAC"]["TS Name"] = [ts_id[x[0]] for x in d]
		data3["MSDAC"]["Track Section Status"] = [x[1] for x in d]
		data3["MSDAC"]["Date"] = [x[2] for x in d]
		data3["MSDAC"]["Time"] = [x[3] for x in d]
		data3["MSDAC"]["Remark"] = [x[4] for x in d]
		
		
		return data3
	# reterive the information from database for the One HASSDAC
	def retrieve_data_for_one_hassdac(self,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql = "select System_ID,System1_Status,System2_Status,Date,Time from HASSDAC_System_Status WHERE System_ID = '"+ID+"'"

		self.execute_query(sql)

		d = self.cursor.fetchall()

				
		data3["HASSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data3["HASSDAC"]["System_ID"] = [x[0] for x in d]
		data3["HASSDAC"]["System1 Status"] = [x[1] for x in d]
		data3["HASSDAC"]["System2 Status"] = [x[2] for x in d]
		data3["HASSDAC"]["Date"] = [x[3] for x in d]
		data3["HASSDAC"]["Time"] = [x[4] for x in d]
		

		return data3

	# reterive the information from database for the DP
	def retrieve_data_for_dp(self,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql = "select DP_ID,DP_Status,Date,Time,Error_Code from DP_Status WHERE System_ID = '"+ID+"'"

		self.execute_query(sql)

		d = self.cursor.fetchall()


		data3["MSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data3["MSDAC"]["DP ID"] = [x[0] for x in d]
		data3["MSDAC"]["DP Status"] = [x[1] for x in d]
		data3["MSDAC"]["Date"] = [x[2] for x in d]
		data3["MSDAC"]["Time"] = [x[3] for x in d]
		data3["MSDAC"]["Error Code"] = [x[4] for x in d]
		

		return data3
		
	#reterive the information for particular ID
	def retrieve_data_for_one_ID(self,ID):
		data2 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql = "select System_ID,Station_Name,System_Status,No_of_DP,No_of_TS,Date,Time FROM System_Information WHERE System_ID = '"+ID+"'"
		self.execute_query(sql)
		d = self.cursor.fetchall()


		data2["MSDAC"]["MSDAC ID"] = [x[0] for x in d]
		data2["MSDAC"]["Station Name"] = [x[1] for x in d]
		data2["MSDAC"]["Status"] = [x[2] for x in d]
		data2["MSDAC"]["No. of DP"] = [x[3] for x in d]
		data2["MSDAC"]["No. of TS"] = [x[4] for x in d]
		data2["MSDAC"]["Date"] = [x[5] for x in d]
		data2["MSDAC"]["Time"] = [x[6] for x in d]

		return data2

	#reterieve history information of HASSDAC
	def retrieve_data_for_hassdacid(self,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}

		sql = "select System_ID,System1_Status,System2_Status,Date,Time from History_Information WHERE System_ID = '"+ID+"' ORDER BY Date DESC, Time DESC"
		self.execute_query(sql)
		d = self.cursor.fetchall()
		data3["HASSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data3["HASSDAC"]["System_ID"] = [x[0] for x in d]
		data3["HASSDAC"]["System1 Status"] = [x[1] for x in d]
		data3["HASSDAC"]["System2 Status"] = [x[2] for x in d]
		data3["HASSDAC"]["Date"] = [x[3] for x in d]
		data3["HASSDAC"]["Time"] = [x[4] for x in d]
		return data3
	
	
