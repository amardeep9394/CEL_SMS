#!/usr/bin/python

import MySQLdb
# searching of the data will start
class Search_Data():
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
	# Searching on the basis of the location
	def search_Data_for_Location(self,loc):
		
		sql="select * from System_Information where Division = '"+loc+"'"
		
		self.execute_query(sql)
		d = self.cursor.fetchall()
		
		#count different system types
		count_msdac = 0
		count_hassdac = 0
		count_ssdac = 0
		
		for x in d:
			if x[2] == 'MSDAC':
				count_msdac += 1
			if x[2] == 'HASSDAC':
				count_hassdac += 1
			if x[2] == 'SSDAC':
				count_ssdac += 1

		self.search_with_loc_and_system_type(loc,'MSDAC')
	# Searching on the basis of the location and system type
	def search_with_loc_and_system_type(self,loc,systype):
		
		sql="select * from System_Information where Division = '"+loc+"' and System_Type = '"+systype+"'"

		self.execute_query(sql)
		d = self.cursor.fetchall()

	def search_result(self,sql):
		# execute query and fetch result
		self.execute_query(sql)
		result = self.cursor.fetchall()

		return result
	# show the history of the data by using the MSDAC ID and the dates
	def history_details(self,sdate,edate,ID,Region):
		
		sql="select * from History_Information where System_ID = '"+ID+"' and Date between '"+sdate+"' and '"+edate+"' and Region = '"+Region+"'"
		self.execute_query(sql)
		d = self.cursor.fetchall()
		return d
	# show the history of the track section details by using the MSDAC ID and the dates	
	def history_msdac_ts_details(self,sdate,edate,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql="select * from TS_Status where System_ID = '"+ID+"' and Date between '"+sdate+"' and '"+edate+"'"

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
		data3["MSDAC"]["Track Section Status"] = [x[2] for x in d]
		data3["MSDAC"]["Date"] = [x[3] for x in d]
		data3["MSDAC"]["Time"] = [x[4] for x in d]
		data3["MSDAC"]["Remark"] = [x[5] for x in d]
		return data3
	# show the history of the DP details by using the MSDAC ID and the dates
	def history_msdac_dp_details(self,sdate,edate,ID):
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}
		sql="select * from DP_Status where System_ID = '"+ID+"' and Date between '"+sdate+"' and '"+edate+"'"

		self.execute_query(sql)
		d = self.cursor.fetchall()
				
		data3["MSDAC"]["S No."] = [i for i in range(1,len(d)+1)]
		data3["MSDAC"]["DP ID"] = [x[0] for x in d]
		data3["MSDAC"]["DP Status"] = [x[2] for x in d]
		data3["MSDAC"]["Date"] = [x[3] for x in d]
		data3["MSDAC"]["Time"] = [x[4] for x in d]
		data3["MSDAC"]["Error Code"] = [x[5] for x in d]
		return data3
	# show the history of the status of track section details by using the TS ID and the dates
	def history_msdac_of_one_ts(self,msdac_id,ts_name):
		sql = "select TS_ID from Match_TS where TS_Name = '"+ts_name+"'"
		self.execute_query(sql)
		d1 = self.cursor.fetchall()
             	
		sql = "Select TS_Status,Date,Time,Remarks from History_Information where TS_ID = '"+d1[0][0]+"'and System_ID = '"+msdac_id+"' ORDER BY Date DESC, Time DESC"
		self.execute_query(sql)
		d2 = self.cursor.fetchall()
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}

		data3["MSDAC"]["S No."] = [i for i in range(1,len(d2)+1)]
		data3["MSDAC"]["TS Name"]= ts_name
		data3["MSDAC"]["Track Section Status"] = [x[0] for x in d2]
		r = [str(x[1]).split("-") for x in d2]

		
		data3["MSDAC"]["Date"] = [r1[-1]+"-"+r1[-2]+"-"+r1[-3] for r1 in r]
		data3["MSDAC"]["Time"] = [x[2] for x in d2]
		data3["MSDAC"]["Remark"] = [x[3] for x in d2]
		

		return data3
	# show the history of the one dp status details by using the DP ID and the dates
	def history_msdac_of_one_dp(self,msdac_id,dp_id):
				
		sql = "Select DP_Status,Date,Time,Error_Code from History_Information where DP_ID = '"+dp_id+"'and System_ID = '"+msdac_id+"' ORDER BY Date DESC, Time DESC"
		self.execute_query(sql)
		d2 = self.cursor.fetchall()
		data3 = {"MSDAC":{},"HASSDAC":{},"SSDAC":{}}

		data3["MSDAC"]["S No."] = [i for i in range(1,len(d2)+1)]
		data3["MSDAC"]["DP ID"]= dp_id
		data3["MSDAC"]["DP Status"] = [x[0] for x in d2]
		data3["MSDAC"]["Date"] = [x[1] for x in d2]
		data3["MSDAC"]["Time"] = [x[2] for x in d2]
		data3["MSDAC"]["Error Code"] = [x[3] for x in d2]
		
		return data3
		
