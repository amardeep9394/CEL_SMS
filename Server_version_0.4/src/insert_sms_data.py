#!/usr/bin/python2
import re
import MySQLdb
#class to process the sms_data
class sms_process():
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
	# function to search the matching error message with the help of hexadecimal error code.
	def get_error_msg(self, code):

		error_msg = {
            '0x00': 'Normal',
	    '0x0': 'Normal',
            '0x11': 'ROM Test During POST',
            '0x12': 'RAM Test During POST',
            '0x13': 'Serial POrt Test During POST',
            '0x14': 'Card Presense Test During POST',
            '0x15': 'Relay Test During POST',
            '0x21': 'ROM Test Failed During System Working',
            '0x22': 'RAM Test Failed During System Working',
            '0x24': 'Card Presence Failed During System Working',
            '0x30': 'Loss of carrier or Link',
            '0x31': 'Sequence of Error Mismatch',
            '0x32': 'Self Count Mismatch',
            '0x33': 'Movement of Train before Preparatory Reset',
            '0x34': 'Outcount Registered before Incount',
            '0x35': 'Negative Count',
            '0x36': 'Shunt Error',
            '0x37': 'Supervisory Error',
            '0x38': 'Internal Shunt Error',
            '0x39': 'Count Mismatch in MLB of same unit',
            '0x40': 'Corruption of Packets - Communication Error',
            '0x41': 'Corruption of Data - CRC Error',
            '0x42': 'COrruption of Data - End of Packet Corrupted',
            '0x43': 'Wheel Shunt Error',
            '0x44': 'Non-overlappig Pulse Found in Forward Direction',
            '0x45': 'Non-overlappig Pulse Found in Reverse Direction',
            '0x46': 'Exit Mismatch - Train IN Trolley OUT or Vice-Versa',
            '0x47': 'Following Trolley Shunt Back',
            '0x48': 'Train Enters After Motor Trolley',
            '0x50': 'Relay Error During POST in Clear State',
            '0x51': 'Relay Error During POST in Occupied State',
            '0x52': 'Relay Contact not Read Back in Clear State',
            '0x53': 'Relay Contact not Read Back in Occupied State',
            '0x60': 'Corruption of SW in Micro-controllers',
            '0x61': 'MLB Decision Mismatch',
            '0x62': 'Secondary CPU Failed',
            '0x66': 'Micro-controller\'s Watchdog Timer Reset',
            '0x70': 'Change in COnfiguration During POST',
            '0x71': 'J Packet Configuration Error',
            '0x72': 'R Packet Configuration Error',
            '0x73': 'Address Changed During System Working',
            '0x74': 'U Packet Configuration Error',
            '0x80': 'Error in Remote System',
            '0x7F': 'Remote Unit is Reset, Local is Not',
            '0x3F': 'Local Unit is Reset, Remote is Not'
            }
		
		if code in error_msg:
        		return error_msg[code]
		else:
			return "Undefined Error Code"
    

	# Check that the SMS contains which packet and break that packet according to their type	
	def break_sms_data(self,str1):

		if '%H' in str1:
			str1 = str1.replace('\n','')
			str1 = str1.replace('%H','')
			str1 = str1.replace('$','')
			lst1 = str1.split(',')

			self.process_sms_data_for_H_Packet(lst1)
			

		if '%D' in str1 or '%T' in str1:	
			str1 = str1.replace('\n','')
			lst1 = str1.split(',')
			lst2 = lst1[3].split('%')
			lst3 = []
			for data in lst2[1:] :
				lst3.append("%"+data)
                        
			self.process_sms_data_for_D_Packet(lst1[0:3]+lst3)
	# Process the data received from the D Packet	
	def process_sms_data_for_D_Packet(self,lst):
		mob_no = lst[0]
		# Check the mobile number exits in database or not
		sql = "select * from System_Information where Mobile_number = '"+mob_no+"'"
		self.execute_query(sql)
		d = self.cursor.fetchone()

		if d == 'none':
			pass
		
		else:
	
			region = d[0]
			div = d[1]
			sys_type = d[2]
			stn_name = d[3]		
			sys_id = d[4]
			sytem_sts = d[-1]
			date = lst[1].replace('/','-')
			time = lst[2]

			self.insert_system_status(region,div,sys_type,sys_id,sytem_sts,date,time)

			for s in lst[3:]:
				# condition to checking for the D packet
				if s[0:2] == '%D' and s[-1] == '$' and len(s) == 16:
					card_no = s[2]
					channel_no = s[3]
					dp_id = card_no+channel_no
					check = self.check_dp_id(dp_id,sys_id)
					error_code = s[5:7]
					e_code = self.get_error_msg(hex(int(error_code)))

					
					# condition to check the dp_id
					if len(check) == 0:

						sql = "INSERT INTO DP_Status (DP_ID,System_ID,DP_Status,Date,Time,Error_Code) VALUES ('"+dp_id+"','"+sys_id+"','"+""+"','"+date+"','"+time+"','"+e_code+"')"
						self.execute_query(sql)
					else:
						sql = "UPDATE DP_Status SET  Date = '"+date+"', Time = '"+time+"',Error_Code = '"+e_code+"' WHERE DP_ID = '"+dp_id+"' AND System_ID = '"+sys_id+"'"
						self.execute_query(sql)
				

					self.Insert_History_for_DP(sys_id,stn_name,date,time,region,div,mob_no,dp_id,sys_type,sytem_sts,e_code)	

				#condition to check for T packet
				if s[0:2] == '%T' and s[-1] == '$' and len(s) == 13:
					card_no = s[2]
					tc_no = s[3]
					ts_id = card_no+tc_no
					check = self.check_ts_id(ts_id,sys_id)
					status = s[4:7]
					sts_binary = '{0:012b}'.format(int(status,16))
					err = self.ts_error_lst(sts_binary,sytem_sts)
					remark = err[0]
					ts_sts = err[1]
					sys_status = err[2]

					# condition to check the dp_id
					if len(check) == 0:

						sql = "INSERT INTO TS_Status (TS_ID,System_ID,TS_Status,Date,Time,Remarks,Region) VALUES ('"+ts_id+"','"+sys_id+"','"+ts_sts+"','"+date+"','"+time+"','"+remark+"','"+region+"')"
						self.execute_query(sql)
					else:
						sql = "UPDATE TS_Status SET TS_Status = '"+ts_sts+"', Date = '"+date+"', Time = '"+time+"',Remarks = '"+remark+"' WHERE TS_ID = '"+ts_id+"' AND System_ID = '"+sys_id+"'"
						self.execute_query(sql)
					self.Insert_History_for_TS(sys_id,stn_name,date,time,region,div,mob_no,ts_id,ts_sts,sys_type,sys_status,remark)
					self.update_system_informtion(sys_id,date,time,sys_status)
					self.update_system_status(sys_id,date,time,sys_status)
	#insert system status table when new data arrived through
	def insert_system_status(self,region,div,sys_type,sys_id,sytem_sts,date,time):
		sql = "INSERT INTO System_Status(Region, Division, System_Type, System_ID, System_Status, Date,Time) VALUES ('"+region+"', '"+div+"', '"+sys_type+"', '"+sys_id+"', '"+sytem_sts+"','"+date+"','"+time+"')"
		self.execute_query(sql) 
	#update status in system status table
	def update_system_status(self,sys_id,date,time,sys_status):
		sql = "UPDATE System_Status SET System_Status = '"+sys_status+"', Date = '"+date+"', Time = '"+time+"' WHERE System_ID = '"+sys_id+"'"
		self.execute_query(sql)
		
	#update status in system informtion
	def update_system_informtion(self,sys_id,date,time,sys_status):
		sql = "UPDATE System_Information SET System_Status = '"+sys_status+"', Date = '"+date+"', Time = '"+time+"' WHERE System_ID = '"+sys_id+"'"
		self.execute_query(sql)
					
	# condition to check the dp_id
	def check_dp_id(self,dp_id,sys_id):

		sql = "select * from DP_Status where DP_ID = '"+dp_id+"' and System_ID = '"+sys_id+"'"
		self.execute_query(sql)
		d = self.cursor.fetchall()
		
		return d
	
	# checking of the track section id from ts status
	def check_ts_id(self,ts_id,sys_id):
		sql = "SELECT * FROM TS_Status WHERE TS_ID = '"+ts_id+"' AND System_ID = '"+sys_id+"'"
		self.execute_query(sql)
		d = self.cursor.fetchall()

		return d

	# Process the data received from the H Packet
	def process_sms_data_for_H_Packet(self,lst):
		mob_no = lst[0]
		# checking for system id using the mobile no from sms received
		sql = "select * from System_Information where Mobile_number = '"+mob_no+"'"
		self.execute_query(sql)
		d = self.cursor.fetchone()

		if d == None:
			pass
		
		else:
			region = d[0]
			div = d[1]
			sys_type = d[2]
			stn_name = d[3]
			sys_id = d[4]
			mob_no = d[5]
			date = lst[1].replace('/','-')
			time = lst[2]
			if len(lst) == 4:
				sys1_sts = lst[3]
			
				sys2_sts = '--'
				uno = '--'
			if len(lst) == 5:
				sys1_sts = lst[3]
			
				sys2_sts = lst[4]
				uno = '--' 

			if len(lst) == 6:
				sys1_sts = lst[3]
			
				sys2_sts = lst[4]
				uno = lst[5]

			sql = "select * from HASSDAC_System_Status where System_ID = '"+sys_id+"'"
			self.execute_query(sql)
			d = self.cursor.fetchall()

			if len(d) == 0:

				sql = "INSERT INTO HASSDAC_System_Status (System_ID, System1_Status, System2_Status, Date, Time, Unknown) VALUES ('"+sys_id+"','"+sys1_sts+"','"+sys2_sts+"','"+date+"','"+time+"','"+uno+"')"
				self.execute_query(sql)
		
			else:

				sql = "UPDATE HASSDAC_System_Status SET System1_Status = '"+sys1_sts+"',System2_Status = '"+sys2_sts+"',Date = '"+date+"',Time = '"+time+"',Unknown = '"+uno+"' WHERE System_ID = '"+sys_id+"'"
				self.execute_query(sql)
		
			sytem_sts = 'Unknown'
			if sys1_sts =='Ok' and sys2_sts == 'Ok':
				sytem_sts = 'OK'

				sql = "UPDATE System_Information SET System_Status = '"+sytem_sts+"',Date = '"+date+"',Time = '"+time+"' WHERE System_ID = '"+sys_id+"'"
				self.execute_query(sql)

			else:

				sql = "UPDATE System_Information SET System_Status = '"+sytem_sts+"',Date = '"+date+"',Time = '"+time+"' WHERE System_ID = '"+sys_id+"'"
				self.execute_query(sql)
			self.Insert_History_for_HASSDAC(sys_id,stn_name,date,time,region,div,mob_no,sys_type,sytem_sts,uno,sys1_sts,sys2_sts)

	# Insert data into History Information table for HASSDAC
	def Insert_History_for_HASSDAC(self,sys_id,stn_name,date,time,region,div,mob_no,sys_type,sytem_sts,uno,sys1_sts,sys2_sts):

		sql = "INSERT INTO History_Information  (System_ID, Station_Name, Date, Time, Region, Division, Mobile_number, DP_ID, DP_Status, TS_ID, TS_Status, System_Type, TS_Info, System_Status, Unknown, System1_Status, System2_Status) Values ('"+sys_id+"','"+stn_name+"','"+date+"','"+time+"','"+region+"','"+div+"','"+mob_no+"','"+""+"','"+""+"','"+""+"','"+""+"','"+sys_type+"','"+""+"','"+sytem_sts+"','"+uno+"','"+sys1_sts+"','"+sys2_sts+"')"
		self.execute_query(sql)
	# Insert data into History Information table for DP
	def Insert_History_for_DP(self,sys_id,stn_name,date,time,region,div,mob_no,dp_id,sys_type,sytem_sts,e_code):

		sql = "INSERT INTO History_Information  (System_ID, Station_Name, Date, Time, Region, Division, Mobile_number, DP_ID, DP_Status, TS_ID, TS_Status, System_Type, TS_Info, System_Status, Unknown, System1_Status, System2_Status,Error_Code) Values ('"+sys_id+"','"+stn_name+"','"+date+"','"+time+"','"+region+"','"+div+"','"+mob_no+"','"+dp_id+"','"+''+"','"+""+"','"+""+"','"+sys_type+"','"+""+"','"+sytem_sts+"','"+""+"','"+""+"','"+""+"','"+e_code+"')"
		self.execute_query(sql)

	# Insert data into History Information table for TS
	def Insert_History_for_TS(self,sys_id,stn_name,date,time,region,div,mob_no,ts_id,ts_sts,sys_type,sys_status,remark):

		sql = "INSERT INTO History_Information  (System_ID, Station_Name, Date, Time, Region, Division, Mobile_number, DP_ID, DP_Status, TS_ID, TS_Status, System_Type, TS_Info, System_Status, Unknown, System1_Status, System2_Status,Error_Code,Remarks) Values ('"+sys_id+"','"+stn_name+"','"+date+"','"+time+"','"+region+"','"+div+"','"+mob_no+"','"+""+"','"+""+"','"+ts_id+"','"+ts_sts+"','"+sys_type+"','"+""+"','"+sys_status+"','"+""+"','"+""+"','"+""+"','"+""+"','"+remark+"')"
		self.execute_query(sql)

	# Create list of the errors from the bytes of the D packet
	def dp_error_lst(self,sts_binary):

		active_status = 'NO'
		error = 'NO'
		link_error = 'NO'
		comm_error = 'NO'
		count_change = 'NO'
		roll_over = 'NO'
		sync = 'NO'
		dp_reset = 'NO'
		error_lst = []
		if sts_binary[0] == '1':
			active_status = 'YES'
			
			if sts_binary[1] == '1':
				error = 'YES'
				error_lst.append('Error')
			if sts_binary[2] == '1':
				link_error = 'YES'
				error_lst.append('Link Error')
			if sts_binary[3] == '1':
				comm_error = 'YES'
				error_lst.append('Comm Error')
			if sts_binary[4] == '1':
				count_change = 'YES'
				error_lst.append('Count Change')
			if sts_binary[5] == '1':
				roll_over = 'YES'
				error_lst.append('Roll Over')
			if sts_binary[6] == '1':
				sync = 'YES'
				error_lst.append('Sync')
			if sts_binary[7] == '1':
				dp_reset = 'YES'
				error_lst.append('DP Reset')
		else:
			error_lst.append('Inactive')

		err = ','.join(error_lst)

		return err

	# Create list of the errors from the bytes of the T packet
	def ts_error_lst(self,sts_binary,sytem_sts):

		# list contains all the list of errors in DP and TS
		error_lst = []

		sts = ''
		if sts_binary[0] == '1':

			
			if sts_binary[1] == '1':
				error_lst.append('Error(Due to DP)')
			if sts_binary[2] == '1':
				error_lst.append('DACFU SUP')
			if sts_binary[3] == '1':
				error_lst.append('Relay Status')
			if sts_binary[4] == '1':
				error_lst.append('Link Error')
			if sts_binary[5] == '1':
				error_lst.append('Comm Error')
			ts_sts = sts_binary[6:8]
			if ts_sts == '00':
				sts = 'RESET'
			if ts_sts == '01':
				sts ='PREPARATORY RESET'
			if ts_sts == '10':
				sts = 'OCCUPIED'
			if ts_sts == '11':
				sts = 'UNOCCUPIED'
			
		else:
			error_lst.append('Inactive')
			sts = '--'
		# check error
		if ("Error(Due to DP)" or "Link Error" or "Comm Error") in error_lst:
			sytem_sts = "Unknown"

		err = ','.join(error_lst)
		return err,sts,sytem_sts

	def break_serial_data(self,sysid,pkt,date,time):
                
                mob_no = 'NULL'
                sql = "select * from System_Information where System_ID = '"+sysid+"'"
		self.execute_query(sql)
		d = self.cursor.fetchone()

		if d == 'none':
			pass
		
		else:
                        try:
                                region = d[0]
                                div = d[1]
                                sys_type = d[2]
                                stn_name = d[3]		
                                sys_id = d[4]
                                sytem_sts = d[-1]
                                date = str(date)
                                time = str(time)

                                self.insert_system_status(region,div,sys_type,sys_id,sytem_sts,date,time)

                                # condition to checking for the D packet
                                if pkt[0:2] == '%D' and pkt[-1] == '$' and len(pkt) == 18:
                                        card_no = pkt[2]
                                        #if card_no == '2':
                                        if re.match("^[1-5]*$",card_no):
                                                channel_no = pkt[4]
                                                if re.match("^[0-7]*$",channel_no):
                                                        dp_id = card_no+channel_no
                                                        check = self.check_dp_id(dp_id,sys_id)
                                                        error_code = pkt[7:9]
                                                        e_code = self.get_error_msg(hex(int(error_code)))

                                                        # condition to check the dp_id
                                                        if len(check) == 0:
                                                                
                                                                sql = "INSERT INTO DP_Status (DP_ID,System_ID,DP_Status,Date,Time,Error_Code) VALUES ('"+dp_id+"','"+sys_id+"','"+""+"','"+date+"','"+time+"','"+e_code+"')"
                                                                self.execute_query(sql)
                                                        else:
                                                                sql = "UPDATE DP_Status SET  Date = '"+date+"', Time = '"+time+"',Error_Code = '"+e_code+"' WHERE DP_ID = '"+dp_id+"' AND System_ID = '"+sys_id+"'"
                                                                self.execute_query(sql)
                                                        

                                                        self.Insert_History_for_DP(sys_id,stn_name,date,time,region,div,mob_no,dp_id,sys_type,sytem_sts,e_code)	

                                #condition to check for T packet
                                if pkt[0:2] == '%T' and pkt[-1] == '$' and len(pkt) == 15:
                                        
                                        card_no = pkt[2]
                                        #if card_no == '2':
                                        if re.match("^[1-5]*$",card_no):
                                                tc_no = pkt[4]
                                                if re.match("^[0-7]*$",tc_no):
                                                
                                                        ts_id = card_no+tc_no
                                                        check = self.check_ts_id(ts_id,sys_id)
                                                        status = pkt[5:8]
                                                        sts_binary = '{0:012b}'.format(int(status,16))
                                                        err = self.ts_error_lst(sts_binary,sytem_sts)
                                                        remark = err[0]
                                                        ts_sts = err[1]
                                                        sys_status = err[2]
                                                        # condition to check the dp_id
                                                        if len(check) == 0:
                                                                
                                                                sql = "INSERT INTO TS_Status (TS_ID,System_ID,TS_Status,Date,Time,Remarks,Region) VALUES ('"+ts_id+"','"+sys_id+"','"+ts_sts+"','"+date+"','"+time+"','"+remark+"','"+region+"')"
                                                                self.execute_query(sql)
                                                        else:
                                                                sql = "UPDATE TS_Status SET TS_Status = '"+ts_sts+"', Date = '"+date+"', Time = '"+time+"',Remarks = '"+remark+"' WHERE TS_ID = '"+ts_id+"' AND System_ID = '"+sys_id+"'"
                                                                self.execute_query(sql)
                                                        self.Insert_History_for_TS(sys_id,stn_name,date,time,region,div,mob_no,ts_id,ts_sts,sys_type,sys_status,remark)
                                                        self.update_system_informtion(sys_id,date,time,sys_status)
                                                        self.update_system_status(sys_id,date,time,sys_status)
                        except:
                                pass

