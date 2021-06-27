#!/usr/bin/python
import MySQLdb
import time
# class to generate the report, extract information like packets, track section error codes, error message etc.
class insert():
	# Open database connection
	def __init__(self):
		self.db = MySQLdb.connect('localhost','root','cel123','remote_monitor_v1')
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor()


		self.d_t_data = {"TS_Data":[],"DP_Data":[],"Config_Data":[]}
		self.t_packet = []
		self.d_packet = []
		self.c_packet = []
		

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
	#search error msg with the help of the ts_error code
	def get_ts_error(self,code):
		error_msg ={
		'0x0': 'Normal',
            	'0x00': 'Normal',
		'0x01' : 'ROM CHECK',
		'0x02' : 'RAM CHECK',
		'0x05' : 'RAM CHECK DURING SYSTEM WORKING',
		'0x06' : 'RELAY CARD TEST DURING POST',
		'0x0D' : 'FPGA MEMORY CHECK',
		'0x0E' : 'CARD NO IS GREATER THAN 5',
		'0x0F' : 'CPU NO IS GREATER THAN 3',
		'0x1F' : 'CONFIG CARD NOT PRESENT AT POWER ON',
		'0x20' : 'CHECK FPGA PORT READ/WRITE AT POWER ON',
		'0x32' : 'SIGNATURE MISMATCH WITH ADJACENT CPUs',
		'0x33' : 'FPGA MEMORY CHECK DURING WORKING',
		'0x34' : 'DACFU BLOCK ADDRESS CHECK DURING WORKING',
		'0x10' : 'NEGATIVE COUNT CHECK DURING WORKING',
		'0x11' : 'RELAY OPEN CHECK DURING WORKING',
		'0x12' : 'RELAY ERROR CHECK DURING WORKING',
		'0x13' : 'RELAY UNOCCUPIED CHECK DURING WORKING',
		'0x14' : 'RELAY OCCUPIED CHECK DURING WORKING',
		'0x16' : 'DP NOT RESETTED, AFTER APPLYING RESET FROM SM PANEL',
		'0x17' : 'FINAL UNOCCUPIED EVAL MISMATCH',
		'0x18' : 'FINAL OCCUPIED EVAL MISMATCH',
		'0x20' : 'LOSS OF CARRIER OR LINK OPEN',
		'0x21' : 'CORRUPTION OF DATA PACKETS',
		'0x22' : 'INVALID CONFIGURATION',
		'0x23' : 'FIELD UNIT ADDRESS MISMATCH ERROR',
		'0x25' : 'DP UNABLE TO SYNCHRONISE',
		'0x30' : 'ROM TEST DURING SYSTEM WORKING',
		'0x31' : 'SERIAL PORT',
		'0x44' : 'NOP DETECTION',
		'0x45' : 'RELAY CARD NOT PRESENT',
		'0x38' : 'TRACK SECTION NOT CONFIGURED IN BLOCK MODE AND INVOLVE DP HAVING BLOCK MODE ADDRESS SETTINGS',
		'0x41' : 'WATCH DOG RESET ERROR',
		'0x39' : 'CORRUPTION OF SOFTWARE IN MICRO CONTROLLER',
		'0x3A' : 'CPU STATUS MISMATCH WITH ADJACENT CPUs',
		'0x42' : 'SHUNTING IN PREPARATORY RESET',
		'0x55' : 'CPU SELF RESET AT POWER ON'
		}
		if code in error_msg:
        		return error_msg[code]
		else:
			return "Undefined Error Code"
	# function to search the matching error message with the help of hexadecimal error code.
	def get_error_msg(self, code):

		error_msg = {
	    '0x0': 'Normal',
            '0x00': 'Normal',
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
	# searching of the packet in the file
	def search_pkt_in_file(self,file_upload_data,upload_path):
		
		# use database
		sql_query = """USE remote_monitor_v1"""


		

		with open(upload_path,'r') as datafile:
			for str1 in datafile:

				if '%D' in str1 or '%T' in str1 or '%C' in str1:
			
					lis1 = str1.split("%")
					lis2 = []
					lis3 = []
					for data in lis1[1:] :
			    			lis2.append("%"+data)
						lis2[-1] = lis2[-1].strip()

					lis3.append(lis2[0])
					for pkt in lis2[1:]:

						if pkt[0:2] == '%T'or pkt[0:2] == '%D' or pkt[0:2] == '%C' and pkt[-1] == '$':

							lis3.append(pkt)



					for pkt in lis3[1:]:
						date_time = lis3[0]
						if date_time[0:2] == '%t' and date_time[-1] == '$' and len(date_time) == 17:
							dd = date_time[2:4]
							mm = date_time[4:6]
							yy = date_time[6:10]
							yy1 = str(int(yy,16))
							mm1 = str(int(mm,16))
							dd1 = str(int(dd,16))

							if len(mm1) == 2:
								mm = mm1
							else:
								mm = '0'+mm1
							
							if len(dd1) == 2:
								dd = dd1
							else:
								dd = '0'+dd1
							date = dd+'-'+mm+'-'+yy1

							hh = date_time[10:12]
							mm = date_time[12:14]
							ss = date_time[14:16]
							hh1 = str(int(hh,16))
							mm1 = str(int(mm,16))
							ss1 = str(int(ss,16))

							if len(hh1) == 2:
								hh = hh1
							else:
								hh = '0'+hh1

							if len(mm1) == 2:
								mm = mm1
							else:
								mm = '0'+mm1
							
							if len(ss1) == 2:
								ss = ss1
							else:
								ss = '0'+ss1
							time = hh+':'+mm+':'+ss


							

							if pkt[0:2] == '%T' and pkt[-1] == '$' and len(pkt) == 13:

								self.extract_T_packet(date,time,pkt)

							if pkt[0:2] == '%D' and pkt[-1] == '$'and len(pkt) == 16:
							
								self.extract_D_packet(date,time,pkt)
							
							if pkt[0:2] == '%C' and pkt[-1] == '$'and len(pkt) == 10:
							
								self.extract_C_packet(date,time,pkt)
						
				else:
					pass

		data = self.display_uploaded_file() # Display the uploaded file data

		return data
	
	# extract D data from packet
	def extract_D_packet(self,date,time,pkt):
		
		d_pkt = pkt
		card_no = pkt[2]
		channel_no = pkt[3]
		dp_id = card_no+channel_no
		status = pkt[4]
		e_code = pkt[5:7]
		if e_code.isalnum():
			error_code = self.get_error_msg('0x'+e_code)
			
		else:	
			error_code = self.get_error_msg(hex(int(e_code)))
		primary_count = pkt[7:11]
		sync_flag = pkt[11:15]

		self.d_t_data["DP_Data"].append((date,time,d_pkt,card_no,channel_no,dp_id,status,e_code,error_code,primary_count,sync_flag))

		
	# extract T data from packet
	def extract_T_packet(self,date,time,pkt):
		t_pkt = pkt
		card_no = pkt[2]
		tc_no = pkt[3]
		ts_id = card_no + tc_no 
		status = pkt[4:7]

		sts_binary = '{0:012b}'.format(int(status,16))
		err = self.ts_error_lst(sts_binary)
		remark = err[0]
		ts_sts = err[1]
		ts_error = pkt[7:9]
		if ts_error.isalnum():
			error_code = self. get_ts_error('0x'+ts_error)
			
		else:	
			error_code = self.get_ts_error(hex(int(ts_error)))
		sec_bal = pkt[9:12]
		
		self.d_t_data["TS_Data"].append((date,time,t_pkt,card_no,tc_no,ts_id,status,remark,ts_sts,ts_error,error_code,sec_bal,sts_binary))
		
	# extract Configuration data from C packet
	def extract_C_packet(self,date,time,pkt):
		c_pkt = pkt
		card_no = pkt[2]
		cpu_no = pkt[3]
		tc_sts_no = pkt[4]
		tc_binary = '{0:04b}'.format(int(tc_sts_no,16))
		if tc_binary[0] == '1':
			tc_sts = 'Active'
		else:
			tc_sts = 'Inactive'
		tc_no = int(tc_binary[1:4],2)
		sts = pkt[5:7]
		sts_binary = '{0:08b}'.format(int(sts,16))
		PS = sts_binary[0:2]
		if PS == '00':
			sts_ps = 'No Piloting required'
		if PS == '01':
			sts_ps = 'At least one DP Point'
		if PS == '10':
			sts_ps = 'One enter and One exit'
		if PS == '11':
			sts_ps = 'All enter and all exit'
		
		RR = sts_binary[2]
		if RR == '1':
			sts_rr = 'Enabled'
		if RR == '0':
			sts_rr = 'Disabled'

		TSB = sts_binary[3]
		if TSB == '1':
			sts_tsb = 'Block Section Mode'
		if TSB == '0':
			sts_tsb = 'Normal Mode'
		
		LV = sts_binary[4]
		if LV == '1':
			sts_lv = 'Active'
		if LV == '0':
			sts_lv = 'Inactive'
		Block_DP_no = int(sts_binary[5:8],2)
		
		no_of_dp = pkt[7]
		
		c_dp = pkt[8]
		dp_binary = '{0:04b}'.format(int(c_dp,16))
		dp_no = int(dp_binary[1:4],2)
		if dp_binary[0] == '1':

			dp = '+'+str(dp_no)
		else:
			dp = '-'+str(dp_no)
			
		self.d_t_data["Config_Data"].append(( date,time,c_pkt,card_no,cpu_no, tc_sts_no,tc_binary,tc_sts,tc_no,sts,sts_binary, PS,sts_ps,RR, sts_rr,TSB,sts_tsb, LV,sts_lv, Block_DP_no,no_of_dp,c_dp,dp_binary,dp_no,dp))

		
		


	# use to fetch data of T, D Packet from other functions
	def display_uploaded_file(self):

		data3 = {"MSDAC":{"DP_Data":{},"TS_Data":{}, "Config_Data":{}},"HASSDAC":{},"SSDAC":{}}

		data3["MSDAC"]["DP_Data"]["S No."] = [i for i in range(1,len(self.d_t_data["DP_Data"])+1)]
		data3["MSDAC"]["DP_Data"]["Date"] = [x[0] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["Time"] = [x[1] for x in self.d_t_data["DP_Data"]]
		#data3["MSDAC"]["DP_Data"]["Packet"] = [x[2] for x in self.d_t_data["DP_Data"]]
		#data3["MSDAC"]["DP_Data"]["Card_No"] = [x[3] for x in self.d_t_data["DP_Data"]]
		#data3["MSDAC"]["DP_Data"]["Channel_No"] = [x[4] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["DP_ID"] = [x[5] for x in self.d_t_data["DP_Data"]]
		#data3["MSDAC"]["DP_Data"]["Status"] = [x[6] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["Error_Code"] = [x[7] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["Remark"] = [x[8] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["Primary_Count"] = [x[9] for x in self.d_t_data["DP_Data"]]
		data3["MSDAC"]["DP_Data"]["Sync_Flag"] = [x[10] for x in self.d_t_data["DP_Data"]]
		
		data3["MSDAC"]["TS_Data"]["S No."] = [i for i in range(1,len(self.d_t_data["TS_Data"])+1)]
		data3["MSDAC"]["TS_Data"]["Date"] = [x[0] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["Time"] = [x[1] for x in self.d_t_data["TS_Data"]]
		#data3["MSDAC"]["TS_Data"]["Packet"] = [x[2] for x in self.d_t_data["TS_Data"]]
		#data3["MSDAC"]["TS_Data"]["Card_No"] = [x[3] for x in self.d_t_data["TS_Data"]]
		#data3["MSDAC"]["TS_Data"]["TC_No"] = [x[4] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["TS_Name"] = [x[5] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["Status"] = [x[6] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["Error"] = [x[7] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["TS_Status"] = [x[8] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["TS_Error"] = [x[9] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["Remark"] = [x[10] for x in self.d_t_data["TS_Data"]]
		data3["MSDAC"]["TS_Data"]["Sec_Bal"] = [x[11] for x in self.d_t_data["TS_Data"]]
		
		data3["MSDAC"]["Config_Data"]["S No."] = [i for i in range(1,len(self.d_t_data["Config_Data"])+1)]
		data3["MSDAC"]["Config_Data"]["Date"] = [x[0] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Time"] = [x[1] for x in self.d_t_data["Config_Data"]]
		#data3["MSDAC"]["Config_Data"]["Packet"] = [x[2] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Card_No"] = [x[3] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["CPU_No"] = [x[4] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["TC_Status"] = [x[7] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["TC_No"] = [x[8] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_Code"] = [x[9] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_PS"] = [x[12] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_RR"] = [x[14] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_TSB"] = [x[16] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_LV"] = [x[18] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["Status_Block_DP_No"] = [x[19] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["No_of_DP"] = [x[20] for x in self.d_t_data["Config_Data"]]
		data3["MSDAC"]["Config_Data"]["DP"] = [x[24] for x in self.d_t_data["Config_Data"]]

		return data3
		


	# Create list of the errors from the bytes of the T packet
	def ts_error_lst(self,sts_binary):

		error_lst = []
		sts = ''
		if sts_binary[0] == '1':

			if sts_binary[1] == '1':
				error_lst.append('Error(Due to DP)')
			if sts_binary[2] == '0':
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
			if sts_binary[8] == '1':
				error_lst.append('Unused')
			if sts_binary[9] == '1':
				error_lst.append('Count Change')
			if sts_binary[10] == '1':
				error_lst.append('Track Reset')
			if sts_binary[11] == '1':
				error_lst.append('Pilot OK')
			
			
			
		else:
			error_lst.append('Inactive')
			sts = '--'

		err = ','.join(error_lst)
		if len(err) == 0:
			err = '--'
		return err,sts




