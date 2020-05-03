# This file fetches all the specified relations and store in a separated file
# in csv format for next step training.

import pandas as pd
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
	host='127.0.0.1', 
	user= 'root', 			# change to your user name,
	password = 'mck19970824!',		# change to your password
	database='umls',	# change to your database name
	auth_plugin='mysql_native_password')

######## hyperparameters, change these! ###########
RELA_list = ['disease_mapped_to_gene', 'gene_product_has_associated_anatomy', 'contains', 'includes', 'used_by', 'has_access', 'used_for']
file_path = '../ML_data/'
###################################################

for RELA in RELA_list:
	print("counting relation ", RELA)
	mycursor = mydb.cursor(buffered=True)

	mycursor.execute("SELECT * FROM MRREL WHERE RELA=%s;", (RELA,))

	rela_data = mycursor.fetchall()

	cui1_list = []
	cui2_list = []

	for i in rela_data:
		# print(i,"\n")
		CUI1 = i[0]
		mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI1,))
		CUI1_string = mycursor.fetchone()
		
		CUI2 = i[4]
		mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI2,))
		CUI2_string = mycursor.fetchone()

		cui1_list.append(CUI1_string[0])
		cui2_list.append(CUI2_string[0])

	# print(cui1_list)
	# print(cui2_list)	
	df1 = pd.DataFrame(np.array([cui1_list,cui2_list]).T,
	                   columns=['CUI1', 'CUI2'])

	df1.to_csv(RELA+'.csv')


