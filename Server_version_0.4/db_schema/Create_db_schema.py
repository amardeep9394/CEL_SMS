#!/usr/bin/python

import MySQLdb

#This class will create databse and there tables
class Create_schema():
	# create a database
	def __init__(self):
		# Open database connection
		db = MySQLdb.connect("localhost","root","cel123")

		# prepare a cursor object using cursor() method
		self.cursor = db.cursor()

		# check and create database
		try:
			sql_query = """CREATE DATABASE IF NOT EXISTS remote_monitor_v1"""
			self.cursor.execute(sql_query)

		except:
			raise ValueError

	# create table of inside above database
	def create_tables(self):

		# use database
		sql_query = """USE remote_monitor_v1"""
		self.cursor.execute(sql_query)

		# create table for Username Infomration
		sql_query = """CREATE TABLE User_Credential(
				Username varchar(50) NOT NULL, 
				Password varchar(50) NOT NULL, 
				User_type varchar(100),
                Region varchar(100)
				)"""

		self.cursor.execute(sql_query)

		# create table for System Information
		sql_query = """CREATE TABLE System_Information(
				Region varchar(50) NOT NULL, 
				Division varchar(50) NOT NULL, 
				System_Type varchar(15) NOT NULL,
				Station_Name varchar(50),
				System_ID varchar(20) NOT NULL Primary Key,
				Mobile_number varchar(15),
				No_of_DP varchar(200),
				No_of_TS varchar(200),
				Date Date,
				Time Time,
				System_Status varchar(100)
				)"""

		self.cursor.execute(sql_query)

		
		# create table for System Status
		sql_query = """CREATE TABLE System_Status(
				Region varchar(50) NOT NULL, 
				Division varchar(50) NOT NULL,
				System_Type varchar(20),
				System_ID varchar(20) NOT NULL Primary Key ,
				System_Status varchar(50),
				Date Date,
				Time Time,
				Updated_TS_Info varchar(100)
				)"""

		self.cursor.execute(sql_query)

		# create table for History Information
		sql_query = """CREATE TABLE History_Information(
				System_ID varchar(20) NOT NULL,
				Station_Name varchar(50),
				Date Date,
				Time Time,
				Region varchar(50) NOT NULL, 
				Division varchar(50) NOT NULL,
				Mobile_number varchar(15),
				DP_ID varchar(30),
				DP_Status varchar(50),
				Error_Code varchar(200),
				TS_ID varchar(30),
				TS_Status varchar(30),
				Remarks varchar(100),
				System_Type varchar(20),
				TS_Info varchar(100),
				System_Status varchar(50),
				Unknown varchar(30),
				System1_Status varchar(30),
				System2_Status varchar(30)
								
				)"""

		self.cursor.execute(sql_query)

		# create table for DP Information
		sql_query = """CREATE TABLE DP_Status(
				DP_ID varchar(30),
				System_ID varchar(20),
				DP_Status varchar(30),
				Error_Code varchar(200),
				Date Date,
				Time Time
				)"""

		self.cursor.execute(sql_query)

		# create table for Track section Information
		sql_query = """CREATE TABLE TS_Status(
				TS_ID varchar(30),
				System_ID varchar(20),
				TS_Status varchar(30),
				Date Date,
				Time Time,
				Remarks varchar(100),
				Region varchar(50)
				)"""

		self.cursor.execute(sql_query)
		
		# create table for Matching Track section ID
		sql_query = """CREATE TABLE Match_TS(
				TS_ID varchar(3) NOT NULL Primary Key,
				TS_Name varchar(5)
				)"""

		self.cursor.execute(sql_query)
		self.create_TSID()

		# create table for HASSDAC System Status
		sql_query = """CREATE TABLE HASSDAC_System_Status(
				System_ID varchar(20) NOT NULL,
				System1_Status varchar(100),
				System2_Status varchar(100),
				Date Date,
				Time Time,
				Unknown varchar(30)
				)"""

		self.cursor.execute(sql_query)

		# create table for Username Infomration
		sql_query = """CREATE TABLE IF NOT EXISTS sms_data (
				id bigint(20) NOT NULL Primary Key, 
				phone_number varchar(12) NOT NULL, 
				message text NOT NULL,
				dt datetime NOT NULL,
				isnew tinyint(1) NOT NULL,
				processed tinyint(1) NOT NULL Default 0
				)"""

		self.cursor.execute(sql_query)

		

	def create_TSID(self):
		ts_id = {}
		count = 0

		card_no = [str(i) for i in range(1,6)]
		ts_no = [str(j) for j in range(8)]
		ts_name = [str(st)+'T' for st in range(1,41)]

		for k in card_no:
			for t in ts_no:
				ts_id[k+t] = ts_name[count]
				sql_query = "INSERT INTO Match_TS(TS_ID, TS_Name) VALUES ('"+str(k+t)+"','"+ts_name[count]+"')"
				self.cursor.execute(sql_query)
				count += 1


run = Create_schema()
run.create_tables()
