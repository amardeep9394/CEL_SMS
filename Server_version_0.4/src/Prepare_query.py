#!/usr/bin/python
# used to prepare the sql query that is performed on the database
class Prepare_Query():
	def __init__(self):
		print "SS"
	# create the sql query based on the url received
	def search_query(self,url,Region):

		sql_lst = []
		dic = {}

		# split url to get search criteria
		url1 = url.split("?")
		url2 = url1[1].split("&")

		for url_ele in url2:
			data = url_ele.split("=")
			dic[data[0]] = data[1]

		###################################

		# get all the column name and column data requested by user
		col_name = []
		col_data = []

		if dic["loc"] != "":
			col_name.append("Division")
			col_data.append(dic["loc"])
	
		if dic["sysid"] != "":
			col_name.append("System_ID")
			col_data.append(dic["sysid"])

		if dic["stn"] != "":
			col_name.append("Station_Name")
			col_data.append(dic["stn"])

		if dic["systype"] != "Select":
			col_name.append("System_Type")
			col_data.append(dic["systype"])

		if dic["sysstatus"] != "Select":
			col_name.append("System_Status")
			col_data.append(dic["sysstatus"])

		#############################################################

		# create condition based on user request
		condition = ""
		data_lst = []
		for i in range(len(col_name)):
			data_lst.append(col_name[i]+" = '"+col_data[i]+"'")

		condition = ' and '.join(data_lst)

		sql = "SELECT * FROM System_Information WHERE "+condition +" and Region = '"+Region+"'"
		############################################

		return sql

	
