#!/usr/bin/python

from bottle import get, post, request, Bottle, run, auth_basic, template, static_file # or route
from main_function import generate_ts_id
from Show_data import Display_data
from collections import OrderedDict
from Search import Search_Data
from Prepare_query import Prepare_Query
from insert_sms_data import sms_process
from data_insert import insert # class to generate the report, extract information like packets, track section error codes, error message etc.
from insert_data import insert_system_detail # insert the new system into system information table 
import os
import subprocess
import csv

import MySQLdb

#global dictionary for TS_ID matching
match_ts = {'56': '39T', '51': '34T', '50': '33T', '53': '36T', '52': '35T', '24': '13T', '25': '14T', '26': '15T', '27': '16T', '20': '9T', '21': '10T', '22': '11T', '23': '12T', '46': '31T', '47': '32T', '44': '29T', '45': '30T', '42': '27T', '43': '28T', '40': '25T', '41': '26T', '11': '2T', '10': '1T', '13': '4T', '12': '3T', '15': '6T', '14': '5T', '17': '8T', '16': '7T', '33': '20T', '32': '19T', '31': '18T', '30': '17T', '37': '24T', '36': '23T', '35': '22T', '34': '21T', '55': '38T', '54': '37T', '57': '40T'}
match_dp = {'DP26': '42', 'DP27': '43', 'DP24': '40', 'DP25': '41', 'DP22': '36', 'DP23': '37', 'DP20': '34', 'DP21': '35', 'DP28': '44', 'DP29': '45', 'DP31': '47', 'DP30': '46', 'DP33': '51', 'DP32': '50', 'DP35': '53', 'DP34': '52', 'DP37': '55', 'DP36': '54', 'DP39': '57', 'DP38': '56', 'DP19': '33', 'DP18': '32', 'DP13': '25', 'DP12': '24', 'DP11': '23', 'DP10': '22', 'DP17': '31', 'DP16': '30', 'DP15': '27', 'DP14': '26', 'DP7': '17', 'DP6': '16', 'DP5': '15', 'DP4': '14', 'DP3': '13', 'DP2': '12', 'DP1': '11', 'DP0': '10', 'DP9': '21', 'DP8': '20'}
app = Bottle()
dp = {}
config = {}
result1 = ()
URL = ""
Region = ""
admin_url = ""
ab= os.path.dirname(os.getcwd())
path = ab+'/template/'

credential_url = ""
file_upload_data = []
admin_data_lst = []

#This function used to find the color on the bases of Track Section Status
def get_colour(status):
	c = {}
	c['UNOCCUPIED'] = 'green'
	c['OCCUPIED'] = 'red'
	c['ERROR'] = 'orange'
	c['RESET'] = 'white'
	c['PREPARATORY RESET'] = 'yellow'

	try:
		rv = c[status]
	except KeyError:
		rv = 'black'

	return rv
#end get_colour

#it is used to display all the templates with the help of bottle on the browser in server
class Server():	
	@app.route('/')
	def hello():
		try:
			global path
    			return template(path+'main.tpl',lbl="")
		except:
			pass

	#insert data into system information table
	@app.route('/insert_details')
	def insert_data():
		url = request.url
		url1 = url.split("?")
		url2 = url1[1].split("&")
		data_lst = []
		for url_ele in url2:
			data = url_ele.split("=")
			data_lst.append(data[1])
		#print "amardeep",data_lst
		lable = ""
		# check if insert system information form is requested
		if 'sysid' in url and 'reg' in url and 'div' in url and 'systype' in url:

			original_data = []
			# change mobile number format
			# organize data
			for data in data_lst:

				if '+' in data:
					original_data.append(data.replace('+',' '))

				else:
					original_data.append(data)
			original_data[5] = '+91'+original_data[5]
			obj = insert_system_detail()
			obj.sql_query_to_insert(original_data)
			lable = "New System Inserted Successfully"

		try:
			d = Display_data()
			check = d.check_user(admin_data_lst)
			
			pageback = " "
			if len(check) == 1:
				global Region
				
				if len(admin_data_lst) == 3:
					
					Region = admin_data_lst[-1]
					login = 'Admin'
				else:
					
					Region = admin_data_lst[-1]
					login = admin_data_lst[-2]
				
				x = d.retrieve_data_for_table1(Region)

				test = {
					'Total': [x["MSDAC"]["Total"],x["HASSDAC"]["Total"],0],
					'System Type':['MSDAC','HASSDAC','SSDAC'],
					'Ok':[x["MSDAC"]["OK"],x["HASSDAC"]["OK"],0],
					'S. No': ['1','2','3'],
					'Unknown':[x["MSDAC"]["Unknown"],x["HASSDAC"]["Unknown"],0]
				}

				test_cases = len(test['S. No'])
				try:
					global path
					lable = ''
					return template(path+'table_all_sys.tpl',rows = test, cases = test_cases,reg= Region,log=login,lbl=lable)
				except:
					pass

			else:
				pageback = "Enter Correct Details"
				try:
					#global path
					return template(path+'main.tpl',lbl=pageback)
				except:
					pass
		except:
			pass

	#This is the Function to Register New User
	@app.route('/registeruser')
	def hello():
		url = request.url
		
		url1 = url.split("?")
		url2 = url1[1].split("&")
		data_lst = []
		for ele in url2:
			data_lst.append(ele.split("=")[1])

		
		#insert data into the user_credintal table
		rdb1 = MySQLdb.connect('localhost', 'root', 'cel123', 'remote_monitor_v1')
		rcur1 = rdb1.cursor()
		
		#check user
		sql = "select * from User_Credential Where Username = '"+data_lst[0]+"'"
		rcur1.execute(sql)
		user = rcur1.fetchall()
		lable = ""
		if len(user) == 1:
			lable = "User Already Exist"
		else:
			if data_lst[2]=='Admin' :
				sql = "Insert into User_Credential(Username,Password,User_type) values ('"+data_lst[0]+"','"+data_lst[1]+"','"+data_lst[2]+"')"
			else:
				sql = "Insert into User_Credential(Username,Password,User_type,Region) values ('"+data_lst[0]+"','"+data_lst[1]+"','"+data_lst[2]+"','"+data_lst[3]+"');"

			rcur1.execute(sql)
			rdb1.commit()
			lable = "Registered Successfully"
		'''try:
			global path
    			return template(path+'main.tpl',lbl=lable)
		except:
			pass'''
		try:
			d = Display_data()
			check = d.check_user(admin_data_lst)
			
			pageback = " "
			if len(check) == 1:
				global Region
				
				if len(admin_data_lst) == 3:
					
					Region = admin_data_lst[-1]
					login = 'Admin'
				else:
					
					Region = admin_data_lst[-1]
					login = admin_data_lst[-2]
				
				x = d.retrieve_data_for_table1(Region)

				test = {
					'Total': [x["MSDAC"]["Total"],x["HASSDAC"]["Total"],0],
					'System Type':['MSDAC','HASSDAC','SSDAC'],
					'Ok':[x["MSDAC"]["OK"],x["HASSDAC"]["OK"],0],
					'S. No': ['1','2','3'],
					'Unknown':[x["MSDAC"]["Unknown"],x["HASSDAC"]["Unknown"],0]
				}

				test_cases = len(test['S. No'])
				try:
					global path
					lable = ''
					return template(path+'table_all_sys.tpl',rows = test, cases = test_cases,reg= Region,log=login,lbl=lable)
				except:
					pass

			else:
				pageback = "Enter Correct Details"
				try:
					#global path
					return template(path+'main.tpl',lbl=pageback)
				except:
					pass
		except:
			pass


	#Function for homepage and passes data to the html templet
	@app.route('/home')
	def serve_homepage1():

		url = request.url
		
		if "Admin" in url or "User" in url or "Helpdesk" in url:
			global admin_url
			admin_url = url
			url1 = url.split("?")
			url2 = url1[1].split("&")
			#data_lst = []
			global admin_data_lst
			admin_data_lst = []
			for url_ele in url2:
				data = url_ele.split("=")

				admin_data_lst.append(data[1])
			d = Display_data()
			
			check = d.check_user(admin_data_lst)
			
			pageback = " "
			if len(check) == 1:
				global Region
				
				if len(admin_data_lst) == 3:
					
					Region = admin_data_lst[-1]
					login = 'Admin'
				else:
					
					Region = admin_data_lst[-1]
					login = admin_data_lst[-2]
				
				x = d.retrieve_data_for_table1(Region)

				test = {
					'Total': [x["MSDAC"]["Total"],x["HASSDAC"]["Total"],0],
					'System Type':['MSDAC','HASSDAC','SSDAC'],
					'Ok':[x["MSDAC"]["OK"],x["HASSDAC"]["OK"],0],
					'S. No': ['1','2','3'],
					'Unknown':[x["MSDAC"]["Unknown"],x["HASSDAC"]["Unknown"],0]
				}

				test_cases = len(test['S. No'])
				try:
					global path
					lable = ""
					return template(path+'table_all_sys.tpl',rows = test, cases = test_cases,reg= Region,log=login,lbl=lable)
				except:
					pass

			else:
				pageback = "Enter Correct Details"
				try:
					#global path
					return template(path+'main.tpl',lbl=pageback)
				except:
					pass
		'''if "fileToUpload" in url:

			file_upload_data = []
			url1 = url.split("?")
			url2 = url1[1].split("&")
			data_lst = []
			for url_ele in url2:
				data = url_ele.split("=")
				file_upload_data.append(data[1])

			file_name = file_upload_data[2]
			command = ['locate', file_name]
			
			output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
			
			output = output.decode()
			search_results = output.split('\n')
			upload_path = search_results[0]
			obj = insert()
			obj.search_pkt_in_file(file_upload_data,upload_path)

			
		else:
			global credential_url
			credential_url = url
		
		url1 = credential_url.split("?")
		url2 = url1[1].split("&")
		data_lst = []
		for url_ele in url2:
			data = url_ele.split("=")
			data_lst.append(data[1])
		print "amardeep",data_lst
		# check if insert system information form is requested
		if 'sysid' in url and 'reg' in url and 'div' in url and 'systype' in url:

			original_data = []
			# change mobile number format
			# organize data
			for data in data_lst:

				if '+' in data:
					original_data.append(data.replace('+',' '))

				else:
					original_data.append(data)
			original_data[5] = '+91'+original_data[5]
			obj = insert_system_detail()
			obj.sql_query_to_insert(original_data)

		d = Display_data()
		check = d.check_user(data_lst)
		
		pageback = " "
		if len(check) == 1:
			global Region
			
			if len(data_lst) == 3:
				
				Region = data_lst[-1]
				login = 'Admin'
			else:
				
				Region = data_lst[-1]
				login = data_lst[-2]
			
			x = d.retrieve_data_for_table1(Region)

			test = {
				'Total': [x["MSDAC"]["Total"],x["HASSDAC"]["Total"],0],
				'System Type':['MSDAC','HASSDAC','SSDAC'],
				'Ok':[x["MSDAC"]["OK"],x["HASSDAC"]["OK"],0],
				'S. No': ['1','2','3'],
				'Unknown':[x["MSDAC"]["Unknown"],x["HASSDAC"]["Unknown"],0]
			}

			test_cases = len(test['S. No'])
			try:
				global path
				return template(path+'table_all_sys.tpl',rows = test, cases = test_cases,reg= Region,log=login)
			except:
				pass

		else:
			pageback = "Enter Correct Details"
			try:
				#global path
				return template(path+'main.tpl',lbl=pageback)
			except:
				pass'''
	
	
	# Show the details of all the MSDAC Information
	@app.route('/page1/MSDAC')
	def serve_homepage2():
		d = Display_data()
		x = d.retrieve_data_for_table2(Region)
		
		test1 = OrderedDict()
		test1['S. No'] = x["MSDAC"]["S No."]
		test1['MSDAC ID'] = x["MSDAC"]["MSDAC ID"]
		test1['Station Name'] = x["MSDAC"]["Station Name"]
		test1['Status'] = x["MSDAC"]["Status"]
	
		test1['No. of DP'] = x["MSDAC"]["No. of DP"] 
		test1['No. of TS'] = x["MSDAC"]["No. of TS"]
		test1['Date'] = x["MSDAC"]["Date"]
		test1['Time'] = x["MSDAC"]["Time"]
		test_cases1 = len(test1['No. of DP'])
		test_cases2 = len(test1['Status'])
		
		##################################################################################
		rdb = MySQLdb.connect('localhost', 'root', 'cel123', 'remote_monitor_v1')
		rcur = rdb.cursor()
		'''sql = "select * from serial_data where Flag = 0"
		rcur.execute(sql)
		sms=rcur.fetchall()
		for i in range(0,len(sms)):
                        
                        d = sms_process()
                        d.break_serial_data(sms[i][1],sms[i][2],sms[i][3],sms[i][4])
                        id_no = sms[i][0]
			sql_query = "update serial_data set Flag = '1' where id = '"+str(id_no)+"'"

			rcur.execute(sql_query)
			rdb.commit()'''
                '''#fetch_SMS() # run php script afeter every 5 sec
		#update sms data in TS_Status table
		sql = "select * from sms_data where processed = 0"
		rcur.execute(sql)
		sms=rcur.fetchall()
		for i in range(0,len(sms)):
			d = sms_process()
			d.break_sms_data(sms[i][2])
			id_no = sms[i][0]
			sql_query = "update sms_data set processed = '1' where id = '"+str(id_no)+"'"

			rcur.execute(sql_query)
			rdb.commit()'''


		sql = "select * from TS_Status WHERE Region = '"+Region+"'"
		rcur.execute(sql)
		rows = rcur.fetchall()

		tsc = {}
		for r in rows:
			try: 
				tsc[r[1]]
			except KeyError:
				tsc[r[1]] = {}

			tsc[r[1]][r[0]] = {'status': r[2], 'date': r[4], 'time': r[5], 'colour': get_colour(r[2])}

		########################################################################################
		rdb = MySQLdb.connect('localhost', 'root', 'cel123', 'remote_monitor_v1')
		rcur = rdb.cursor()
		if Region == 'Admin':
			sql = "select System_ID, "
			sql += "sum(case when TS_Status='OCCUPIED' then 1 else 0 end) as occupied, "
			sql += "sum(case when TS_Status='UNOCCUPIED' then 1 else 0 end) as clear, "
			sql += "sum(case when TS_Status = 'RESET' then 1 else 0 end) as reset, "
			sql += "sum(case when TS_Status = 'PREPARATORY RESET' then 1 else 0 end) as prep, "
			sql += "sum(case when TS_Status='ERROR' then 1 else 0 end) as error, count(*) as total "
			sql += "from TS_Status group by System_ID"
		
		else:
			sql = "select System_ID, "
			sql += "sum(case when TS_Status='OCCUPIED' then 1 else 0 end) as occupied, "
			sql += "sum(case when TS_Status='UNOCCUPIED' then 1 else 0 end) as clear, "
			sql += "sum(case when TS_Status = 'RESET' then 1 else 0 end) as reset, "
			sql += "sum(case when TS_Status = 'PREPARATORY RESET' then 1 else 0 end) as prep, "
			sql += "sum(case when TS_Status='ERROR' then 1 else 0 end) as error, count(*) as total "
			sql += "from TS_Status  where Region = '"+Region+"' group by System_ID"
		rcur.execute(sql)
		rows = rcur.fetchall()

		tscn = {}
		for r in rows:
			tscn[r[0]] = {}
			tscn[r[0]]['occupied'] = r[1]
			tscn[r[0]]['clear'] = r[2]
			tscn[r[0]]['reset'] = r[3]
			tscn[r[0]]['prep'] = r[4]
			tscn[r[0]]['error'] = r[5]
			tscn[r[0]]['total'] = r[1]+r[2]+r[3]+r[4]+r[5]
		try:
			global path
			return template(path+'table_all_MSDAC.tpl',rows = test1, cases = test_cases1 , case2 = test_cases2, tsc=tsc, tscn=tscn)
		except:
			pass

	# Show the details of all the HASSDAC Information	
	@app.route('/page1/HASSDAC')
	def serve_homepage2():
		
		d = Display_data()
		x = d.retrieve_data_for_hassdac(Region)
		test1 = OrderedDict()
		test1['S. No'] = x["HASSDAC"]["S No."]
		test1['HASSDAC ID'] = x["HASSDAC"]["HASSDAC ID"]
		test1['Station Name'] = x["HASSDAC"]["Station Name"]
		test1['Status'] = x["HASSDAC"]["Status"]

		test1['System1 Status'] = x["HASSDAC"]["System1 Status"]
		test1['System2 Status'] = x["HASSDAC"]["System2 Status"]
		test1['Date'] = x["HASSDAC"]["Date"]
		test1['Time'] = x["HASSDAC"]["Time"]
		test_cases1 = len(test1['S. No'])

		try:
			global path
			return template(path+'table_all_HASSDAC.tpl',rows = test1, cases = test_cases1)
		except:
			pass


	#show the history of one HASSDAC information
	@app.route('/page3/<url:re:.+>/hassdac')
	def server_hassdac(url):
		x = request.url
		ID = x.split("/")[-2]
		d = Display_data()
		x = d.retrieve_data_for_hassdacid(ID)
		test1 = OrderedDict()
		test1['S. No'] = x["HASSDAC"]["S No."]
		test1['HASSDAC ID'] = x["HASSDAC"]["System_ID"]



		test1['System1 Status'] = x["HASSDAC"]["System1 Status"]
		test1['System2 Status'] = x["HASSDAC"]["System2 Status"]
		test1['Date'] = x["HASSDAC"]["Date"]
		test1['Time'] = x["HASSDAC"]["Time"]
		test_cases1 = len(test1['S. No'])

		try:
			global path
			return template(path+'history_one_HASSDAC.tpl',rows = test1, cases = test_cases1,ID=ID)
		except:
			pass

	# Show all the details of all the DP
	@app.route('/page2/<url:re:.+>/dp')
	def serve_homepage3(url):
		x = request.url
		ID = x.split("/")[-2]

		d = Display_data()
		x = d.retrieve_data_for_dp(ID)
		y = d.retrieve_data_for_one_ID(ID)
		test1 = OrderedDict()

		test1['MSDAC ID'] = y["MSDAC"]["MSDAC ID"]
		test1['Station Name'] = y["MSDAC"]["Station Name"]
		test1['Status'] = y["MSDAC"]["Status"]

		test1['No. of DP'] = y["MSDAC"]["No. of DP"]
		test1['No. of TS'] = y["MSDAC"]["No. of TS"]
		test1['Date'] = y["MSDAC"]["Date"]
		test1['Time'] = y["MSDAC"]["Time"]
		test_cases1 = len(test1['No. of DP'])

		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['DP ID'] = x["MSDAC"]["DP ID"]

		test2['Error Code'] = x["MSDAC"]["Error Code"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'table_all_DP.tpl',rows = test2, cases = test_cases2,ID=ID,rows1=test1, cases1 = test_cases1)
		except:
			pass


	# Show all the details of all the TS
	@app.route('/page2/<url:re:.+>/ts')
	def serve_homepage3(url):
		x = request.url
		ID = x.split("/")[-2]

		d = Display_data()
		x = d.retrieve_data_for_table3(ID)
		y = d.retrieve_data_for_one_ID(ID)
		test1 = OrderedDict()
		test1['MSDAC ID'] = y["MSDAC"]["MSDAC ID"]
		test1['Station Name'] = y["MSDAC"]["Station Name"]
		test1['Status'] = y["MSDAC"]["Status"]
		test1['No. of DP'] = y["MSDAC"]["No. of DP"]
		test1['No. of TS'] = y["MSDAC"]["No. of TS"]
		test1['Date'] = y["MSDAC"]["Date"]
		test1['Time'] = y["MSDAC"]["Time"]
		test_cases1 = len(test1['No. of DP'])

		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['TS Name'] = x["MSDAC"]["TS Name"]
		test2['TS Status'] = x["MSDAC"]["Track Section Status"]
		test2['Remark'] = x["MSDAC"]["Remark"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'table_all_TS.tpl',rows = test2, cases = test_cases2,ID=ID, rows1=test1, cases1 = test_cases1 )
		except:
			pass
		




	@app.route('/hello',method=['POST'])
	def hello():


		urlparts = request.urlparts
		if request.auth[0]=='abhi' and request.auth[1]=='masamb':
			print "AUTHORISED USER"
			return "AUTHORISED USER"
		else:
			return "UN-AUTHORISED USER"

	@app.route('/hello/msdacdata',method=['POST'])
	def data():

		urlparts = request.urlparts
		data = request.body.readlines()[0]

		with open('test.py','w') as f:
			f.write(data)
		f.close()
		sd= eval(open('test.py').read())

		d = generate_ts_id()
		d.create_ts_signal(sd)

	@app.route('/hello/msdacsms',method=['POST'])
	def data():

		urlparts = request.urlparts
		sms = request.body.readlines()[0]
		with open('test.py','w') as f:
			f.write(sms)
		f.close()
		sd= open('test.py').read()
                                                                                                            
		d = sms_process()
		d.break_sms_data(sd)
		

	@app.route('/static/<filename:re:.*\.css>', name = 'static')
	def stylesheets(filename):
    		return static_file(filename, root=ab+'/static/')

	@app.route('/static/<filename:re:.*\.png>', name = 'static')
	def stylesheets(filename):
    		return static_file(filename, root=ab+'/static/')
	
	
	#history of Track section of particular MSDAC
	@app.route('/history_result/<url:re:.+>/one_ts')
	def history_of_one_ts(url):
		x = request.url
		msdac_id = x.split("/")[4]
		msdac_id = msdac_id.split("%20")[0]
		ts_name = x.split("/")[-2]
		obj = Search_Data()
		x = obj.history_msdac_of_one_ts(msdac_id,ts_name)
		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['TS Status'] = x["MSDAC"]["Track Section Status"]
		test2['Remark'] = x["MSDAC"]["Remark"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'history_one_ts.tpl',rows = test2, cases = test_cases2,ID=msdac_id,TS_Name=ts_name)
		except:
			pass
		


	#history of Track section of particular MSDAC
	@app.route('/history_result/<url:re:.+>/one_dp')
	def history_of_one_ts(url):
		x = request.url
		msdac_id = x.split("/")[4]
		msdac_id = msdac_id.split("%20")[0]
		dp_name = x.split("/")[-2]
		dp_id = match_dp[x.split("/")[-2]]

		obj = Search_Data()
		x = obj.history_msdac_of_one_dp(msdac_id,dp_id)
		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['Error Code'] = x["MSDAC"]["Error Code"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'history_one_dp.tpl',rows = test2, cases = test_cases2, ID=msdac_id, DP_ID=dp_id, dp_name=dp_name )
		except:
			pass
		 
		
	#history of Track section of particular MSDAC
	@app.route('/history_result/<url:re:.+>/ts')
	def history_of_msdac(url):
		x = request.url
		msdac_id = x.split("/")[-3]
		date = x.split("/")[-2].split("%20")
		sdate = date[1]
		edate = date[3]
		
		obj = Search_Data()
		x = obj.history_msdac_ts_details(sdate,edate,msdac_id)
		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['TS Name'] = x["MSDAC"]["TS Name"]
		test2['TS Status'] = x["MSDAC"]["Track Section Status"]
		test2['Remark'] = x["MSDAC"]["Remark"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'history_MSDAC.tpl',rows = test2, cases = test_cases2, ID=msdac_id, start=sdate, end=edate)
		except:
			pass


	#history of Track section of particular MSDAC
	@app.route('/history_result/<url:re:.+>/dp')
	def history_of_msdac(url):
		x = request.url
		msdac_id = x.split("/")[-3]
		date = x.split("/")[-2].split("%20")
		sdate = date[1]
		edate = date[3]
		
		obj = Search_Data()
		x = obj.history_msdac_dp_details(sdate,edate,msdac_id)
		test2 = OrderedDict()
		test2['S. No'] = x["MSDAC"]["S No."]
		test2['DP ID'] = x["MSDAC"]["DP ID"]
		test2['Error Code'] = x["MSDAC"]["Error Code"]
		test2['Date'] = x["MSDAC"]["Date"]
		test2['Time'] = x["MSDAC"]["Time"]
		test_cases2 = len(test2['S. No'])

		try:
			global path
			return template(path+'history_all_dp.tpl',rows = test2, cases = test_cases2, ID=msdac_id, start=sdate, end=edate )
		except:
			pass

		
		

	#History results
	@app.route('/history_result')
	def history_of_system():
		x = request.url
		
		lst = []
		l = x.split("?")
		p = l[-1].split("&")

		for i in range(3):
			k = p[i].split("=")[-1].replace("%2F","-")# first split on basis of = and then replace string on basis of desired format
			lst.append(k)
		obj = Search_Data()
		d = obj.history_details(lst[0],lst[1],lst[2],Region)
		if len(d) >= 1:
			ID = lst[2]
			sdate = lst[0]
			edate = lst[1]
			stn_name = d[0][1]
			mob_no = d[0][6]
			if d[0][11] == 'MSDAC':

				test = OrderedDict()

				test['S No.'] = [str(i) for i in range(1,len(d)+1)]
				test['Status'] = [x[13] for x in d]
				test['Date'] = [x[2] for x in d]
				test['Time'] = [x[3] for x in d]

				test_cases = len(test['S No.'])
			

				obj = Search_Data()
				sql = "SELECT No_of_DP FROM System_Information WHERE System_ID = '"+lst[2]+"'"
				nod = obj.search_result(sql)[0][0]

				sql = "SELECT No_of_TS FROM System_Information WHERE System_ID = '"+lst[2]+"'"
				nots = obj.search_result(sql)[0][0]

				try:
					global path
					return template(path+'history_msdac_id.tpl',rows = test, cases = test_cases, ID=ID, stn_name=stn_name, nod=nod, nots=nots, sdate=sdate, edate= edate )
				except:
					pass
				

			if d[0][11] == 'HASSDAC':
		
				test = OrderedDict()
				test['S No.'] = [str(i) for i in range(1,len(d)+1)]
				test['Status'] = [x[13] for x in d]
				test['System1 Ststus'] = [x[15] for x in d]
				test['System2 Ststus'] = [x[16] for x in d]
				test['Date'] = [x[2] for x in d]
				test['Time'] = [x[3] for x in d]
				test_cases = len(test['S No.'])

				try:
					#global path
					return template(path+'history_hassdac_id.tpl',rows = test, cases = test_cases, ID=ID,stn_name=stn_name,no=mob_no,sdate=sdate,edate= edate )
				except:
					pass

		else:
			try:
				#global path
				return template(path+'no_result.tpl')
			except:
				pass


	
	@app.route('/dp_info')
	def generate_report():
		
		test_cases2 = len(dp['S. No'])

		try:
			global path
			return template(path+'upload1.tpl',rows = dp, cases = test_cases2,  ID = sys_id_ts, reg = region_ts)
		except:
			pass
		

	@app.route('/config_info')
	def generate_report():
		test_cases2 = len(config['S. No'])
		

		try:
			global path
			return template(path+'upload2.tpl',rows = config, cases = test_cases2,  ID = sys_id_ts, reg = region_ts)
		except:
			pass


	
	
	
	#Generate Report
	@app.route('/generate_report',method = 'POST')
	def generate_report():
		x = request.url
		global sys_id_ts
		global region_ts
		sys_id_ts = request.forms.get('sysid')
		region_ts = request.forms.get('region')
		files = request.files.get('fileToUpload')
		
		files.save("../upload_files",files.filename)

		file_name = files.filename
		
		upload_path = "../upload_files/"+file_name
		obj = insert()
		d = obj.search_pkt_in_file(file_upload_data,upload_path)

		global config
		config = OrderedDict()
		config['S. No'] = d["MSDAC"]["Config_Data"]["S No."]
		config['Date'] = d["MSDAC"]["Config_Data"]["Date"]
		config['Time'] = d["MSDAC"]["Config_Data"]["Time"]
		config['Card_No'] = d["MSDAC"]["Config_Data"]["Card_No"]
		config['CPU_No'] = d["MSDAC"]["Config_Data"]["CPU_No"]
		config['TC_Status'] = d["MSDAC"]["Config_Data"]["TC_Status"]
		config['TC_No'] = d["MSDAC"]["Config_Data"]["TC_No"]
		config['Status_Code'] = d["MSDAC"]["Config_Data"]["Status_Code"]
		config['Piloting_Scheme'] = d["MSDAC"]["Config_Data"]["Status_PS"]
		config['Relay_Read_Back'] = d["MSDAC"]["Config_Data"]["Status_RR"]
		config['Track_Section_Block'] = d["MSDAC"]["Config_Data"]["Status_TSB"]
		config['LV'] = d["MSDAC"]["Config_Data"]["Status_LV"]
		config['Block_DP_No'] = d["MSDAC"]["Config_Data"]["Status_Block_DP_No"]
		config['No_of_DP'] = d["MSDAC"]["Config_Data"]["No_of_DP"]
		config['DP_No'] = d["MSDAC"]["Config_Data"]["DP"]
		
		
		global dp
		dp = OrderedDict()
		dp['S. No'] = d["MSDAC"]["DP_Data"]["S No."]
		dp['Date'] = d["MSDAC"]["DP_Data"]["Date"]
		dp['Time'] = d["MSDAC"]["DP_Data"]["Time"]
		dp['DP ID'] = d["MSDAC"]["DP_Data"]["DP_ID"]
		dp['Error Code'] = d["MSDAC"]["DP_Data"]["Error_Code"]
		dp['Remark'] = d["MSDAC"]["DP_Data"]["Remark"]
		dp['Primary Count'] = d["MSDAC"]["DP_Data"]["Primary_Count"]
		dp['Sync Flag'] = d["MSDAC"]["DP_Data"]["Sync_Flag"]		
		
		global test3
		test3 = OrderedDict()
		test3['S. No'] = d["MSDAC"]["TS_Data"]["S No."]
		test3['Date'] = d["MSDAC"]["TS_Data"]["Date"]
		test3['Time'] = d["MSDAC"]["TS_Data"]["Time"]
		test3['TS Name'] = d["MSDAC"]["TS_Data"]["TS_Name"]
		test3['Status'] = d["MSDAC"]["TS_Data"]["Status"]
		test3['Status Description'] = d["MSDAC"]["TS_Data"]["Error"]
		test3['TS Status'] = d["MSDAC"]["TS_Data"]["TS_Status"]
		test3['TS Error'] = d["MSDAC"]["TS_Data"]["TS_Error"]	
		test3['Remark'] = d["MSDAC"]["TS_Data"]["Remark"]
		
		test_cases3 = len(test3['S. No'])
		try:
			global path
			return template(path+'upload.tpl', rows1= test3, cases1 = test_cases3, ID = sys_id_ts, reg = region_ts)
		except:
			pass


		

	@app.route('/export_csv',method = 'POST')
	def generate_report():
		
		test_cases3 = len(test3['S. No'])
		#code for the csv file of TS Information
		f = open("log.py","w")
		f.write(repr(test3)+'\n')
		f.close()
		
		data = eval(open('log.py').read())
		k = data.values()
		# make all list of equal length
		max_len = max(map(len,k))
		mod_data=[]
		for row in k:
			m = len(row)
			for i in range(max_len):
				if len(row) < max_len:
					row.append('')
					m +=1
			mod_data.append(row)
		# write data column wise to csv file 
		with open('../csv_files/'+sys_id_ts+'_'+region_ts+'_TS.csv','wb') as f:
			w=csv.DictWriter(f,data.keys())
			w.writeheader()
			writer = csv.writer(f)
			writer.writerows(zip(mod_data[0],mod_data[1],mod_data[2],mod_data[3],mod_data[4],mod_data[5],mod_data[6],mod_data[7],mod_data[8]))

		#code for the csv file of DP Information
		f = open("log.py","w")
		f.write(repr(dp)+'\n')
		f.close()
		
		data = eval(open('log.py').read())
		k = data.values()
		# make all list of equal length
		max_len = max(map(len,k))
		mod_data=[]
		for row in k:
			m = len(row)
			for i in range(max_len):
				if len(row) < max_len:
					row.append('')
					m +=1
			mod_data.append(row)
		# write data column wise to csv file 
		with open('../csv_files/'+sys_id_ts+'_'+region_ts+'_DP.csv','wb') as f:
			w=csv.DictWriter(f,data.keys())
			w.writeheader()
			writer = csv.writer(f)
			writer.writerows(zip(mod_data[0],mod_data[1],mod_data[2],mod_data[3],mod_data[4],mod_data[5],mod_data[6],mod_data[7]))

		#code for the csv file of Config Information
		f = open("log.py","w")
		f.write(repr(config)+'\n')
		f.close()
		
		data = eval(open('log.py').read())
		k = data.values()
		# make all list of equal length
		max_len = max(map(len,k))
		mod_data=[]
		for row in k:
			m = len(row)
			for i in range(max_len):
				if len(row) < max_len:
					row.append('')
					m +=1
			mod_data.append(row)
		# write data column wise to csv file 
		with open('../csv_files/'+sys_id_ts+'_'+region_ts+'_Config.csv','wb') as f:
			w=csv.DictWriter(f,data.keys())
			w.writeheader()
			writer = csv.writer(f)
			writer.writerows(zip(mod_data[0],mod_data[1],mod_data[2],mod_data[3],mod_data[4],mod_data[5],mod_data[6],mod_data[7],mod_data[8],mod_data[9],mod_data[10],mod_data[11],mod_data[12],mod_data[13],mod_data[14]))

		try:
			global path
			return template(path+'upload.tpl', rows1= test3, cases1 = test_cases3, ID = sys_id_ts, reg = region_ts)
		except:
			pass


		

	
	@app.route('/UploadFiles', method='POST')
	def UploadFiles():
	   	uploadinc = request.files.get('uploadinc')

	   	uploadinc.save("C:\Users\cel-admin\Desktop/"+uploadinc.filename)
	
	@app.route('/tsd/<state>/<sid>')
	def ts_detail(state, sid):
		global match_ts
		rdb = MySQLdb.connect('localhost', 'root', 'cel123', 'remote_monitor_v1')
		rcur = rdb.cursor()
		sql = "select No_of_DP,No_of_TS from System_Information where System_ID='" + sid + "'"
		rcur.execute(sql)
		info = rcur.fetchall()
		ts_dp_detail = info[0][0].replace('%3A',':').split('%2C')
		dp_detail = {}
		for d in ts_dp_detail:
			data = d.split('-')
			dp_detail[data[0]] = data[1].split(':')
		sql = "select TS_ID, Date, Time from TS_Status where System_ID='" + sid + "' and TS_Status = '" + state + "'"
		rcur.execute(sql)
		rows = rcur.fetchall()
                
		rv = {}
		for r in rows:
                        try:
                                rv[match_ts[r[0]]] = {} #TS_ID


                                # change date formate to dd-mm-yyyy
                                x = str(r[1]).split("-")
                                rv[match_ts[r[0]]]['date'] = x[-1]+"-"+x[-2]+"-"+x[-3]
                                rv[match_ts[r[0]]]['time'] = r[2] #Time
                                if match_ts[r[0]] in dp_detail:
                                        rv[match_ts[r[0]]]['dp'] = dp_detail[match_ts[r[0]]]
                                else:
                                        pass
                        except:
                                pass

		
		title = ""
		tdata = {
			'RESET': 'Track Sections in Reset State', 
			'OCCUPIED': 'TS in Occupied State', 
			'UNOCCUPIED': 'TS in Unoccupied State', 
			'ERROR': 'TS in Error State',
			'PREPARATORY RESET': 'TS in Prep State'
		}
		try:
			global path
			return template(path+'tsd.tpl', rv=rv, sid=sid, title=tdata[state])
		except:
			pass


        @app.route('/fetch_sms')
	def fetch_SMS():

	   	os.system('php /var/www/html/protect_fetch/fetch.php')

if __name__ == '__main__':
	run(app, host='127.0.0.1', port=8080, debug = False)




