#!/usr/bin/python
import time
from insert_ts_status import Db_process
# class to convert ts_name to ts_id
class generate_ts_id():
	
	#function to generate the track section signal	
	def create_ts_signal(self,sd):
		dic = {}
		data_card1 = {}
		data_card2 = {}
		data_card3 = {}
		data_card4 = {}
		data_card5 = {}

		ts_signal = {"Green":"UNOCCUPIED","Red":"ERROR","#FF5733":"RESET","Yellow":"PREPARATORY RESET","Orange":"OCCUPIED"}

		keys = [str(st)+'T' for st in range(1,41)]


		data = sd#eval(open("msdState.json").read())

		ln = data["data"].keys()
		for i, key in enumerate(keys):
		    if key in ln:
			if i <= 7:
			    data_card1[key] = ts_signal[data["data"][key]]
			    
			if i >7 and i <= 15:
			    data_card2[key] = ts_signal[data["data"][key]]
			    
			if i >15 and i <= 23:
			    data_card3[key] = ts_signal[data["data"][key]]
			    
			if i >23 and i <= 31:
			    data_card4[key] = ts_signal[data["data"][key]]
			    
			if i >31 and i <= 39:
			    data_card5[key] = ts_signal[data["data"][key]]

		dic["Card1"]=data_card1
		dic["Card2"]=data_card2
		dic["Card3"]=data_card3
		dic["Card4"]=data_card4
		dic["Card5"]=data_card5

		x = self.create_ts_id(data,ln,ts_signal)
		return x

	#function to generate the track section id with their status
	def create_ts_id(self,data,ln,ts_signal):
		ts_id = {}
		count = 0
		card_no = [str(i) for i in range(1,6)]
		ts_no = [str(j) for j in range(8)]
		ts_name = [str(st)+'T' for st in range(1,41)]

		for k in card_no:
			for t in ts_no:
				ts_id[k+t] = ts_name[count]

				if ts_name[count] in ln:
					ts_id[k+t]= ts_signal[data["data"][ts_name[count]]]
				
				else:
					ts_id[k+t] = "NULL"

				count += 1

		ts_id["System_ID"] = data["System_no"]
		ts_id["Date"]= time.strftime("%Y-%m-%d")
		ts_id["Time"]= time.strftime("%H:%M:%S")
		ts_id["Station_Name"] = data["Station"]

		temp = Db_process(ts_id)

		return temp

