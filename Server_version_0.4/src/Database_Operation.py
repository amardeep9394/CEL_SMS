#!/usr/bin/python

import MySQLdb
#class for the database operation
class Db_Operation():
	# Open database connection
	def __init__(self):
		self.db = MySQLdb.connect('localhost','root','cel123','remote_monitor_v1')
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor()

	# Process the data enter by User based on sql query
	def process_request(self,lst_of_data):

		self.lst_of_data = lst_of_data


		# list of the data that contains all the information about the table_name, column name, condition and data
		p_data = list(self.break_data(self.lst_of_data))

		if self.lst_of_data[0] == "INSERT":
			status = self.insert(p_data)
			
		elif self.lst_of_data[0] == "SELECT":
			status = self.select(p_data)
			
		elif self.lst_of_data[0] == "UPDATE":
			status = self.update(p_data)

		elif self.lst_of_data[0] == "DELETE":
			status = self.delete(p_data)


		return status

	# Break the user data for insertion, updation, selection purpose
	def break_data(self,data_lst):
		

		# get table name
		table_name = data_lst[1]
		
		# get column name
		# if processing is in one or two columns
		if self.lst_of_data[0] == "INSERT":
			# for all columns
			col = eval(open('column.py').read())
			col = col[data_lst[1]]
			self.col_len = len(col)
			column_name = ",".join(col)

		elif data_lst[2] == ["*"]:
			column_name = "*"
		else:
			column_name = data_lst[2]

		# get condition
		condition = ""
		if self.lst_of_data[0] == "SELECT" and self.lst_of_data[3] == []:
			condition = ""

		else:
			condition = "".join(data_lst[3])
			
		# get data
		data = self.lst_of_data[4]

		# convert all data into string
		d = []
		for e in data:
			d.append(str(e))

		self.lst_of_data[4] = d
		if self.lst_of_data[0] == "INSERT":

			data = tuple(self.lst_of_data[4])

		elif self.lst_of_data[0] == "UPDATE":
			
			pass

		return table_name,column_name,condition,data

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

	# to fetch the data
	def select(self,lst):
		
		table_name = lst[0]
		column_name = lst[1]
		condition = lst[2]
		
		sql = "SELECT "+column_name+" FROM "+table_name+ " " +condition

		self.execute_query(sql)
		d = self.cursor.fetchall()

		return d
	#insert the data into tables of database
	def insert(self,lst):

		table_name = lst[0]
		column_name = lst[1]
		condition = lst[2]
		data = lst[3]
		
		sql = "INSERT INTO "+str(table_name)+"("+str(column_name)+") values"+str(data)

		self.execute_query(sql)
		
		return "Success"
