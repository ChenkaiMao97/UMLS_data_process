# This file fetches all the specified relations and store in a separated file
# a dictionary for all the relationships

import pandas as pd
import numpy as np
import progressbar
import mysql.connector

mydb = mysql.connector.connect(
	host='127.0.0.1', 
	user= 'root', 			# change to your user name,
	password = 'mck19970824!',		# change to your password
	database='umls',	# change to your database name
	auth_plugin='mysql_native_password')

######## hyperparameters, change these! ###########
RELA = 'isa'
file_path = '../ML_data/'
file_name = 'isa.csv'
###################################################

mycursor = mydb.cursor(buffered=True)

mycursor.execute("SELECT * FROM MRREL WHERE RELA=%s;", (RELA,))

rela_data = mycursor.fetchall()

rela_dic = dict()

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range(len(rela_data)):
	# print(i,"\n")
	perc = int(i/len(rela_data)*100)
	bar.update(perc)
	CUI1 = rela_data[i][0]
	mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI1,))
	CUI1_string = mycursor.fetchone()
	
	CUI2 = rela_data[i][4]
	mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI2,))
	CUI2_string = mycursor.fetchone()

	if CUI1_string[0] in rela_dic:
		rela_dic[CUI1_string[0]].append(CUI2_string[0])
	else:
		rela_dic[CUI1_string[0]] = [CUI2_string[0]]

bar.finish()
print(rela_dic)


import json
json_data = json.dumps(rela_dic)
f = open("isa_dict.json","w")
f.write(json_data)
f.close()