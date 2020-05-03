# import mysql.connector

# mydb = mysql.connector.connect(
# 	host='127.0.0.1', 
# 	user= 'root', 			# change to your user name,
# 	password = 'mck19970824!',		# change to your password
# 	database='umls',	# change to your database name
# 	auth_plugin='mysql_native_password')

# ######## hyperparameters, change these! ###########
# RELA = 'isa'
# file_path = '../ML_data/'
# file_name = 'isa.csv'
# ###################################################

import json
import random
import pandas as pd
import numpy as np
import progressbar

with open('isa_dict.json') as file:
	rela_dict = json.loads(file.read())

with open('CUI1.json') as file:
	CUI1_list = json.loads(file.read())

with open('CUI2.json') as file:
	CUI2_list = json.loads(file.read())


def find_similar(target, corpus, n):
	# find top n phrases in corpus that contains the most common words as the target
	target_words = set(target.split())

	top_n_words = [(-1,' ')]*n
	for i in corpus:
		if i==target:
			continue
		sample_words = set(i.split())
		common = len(target_words & sample_words)
		if common > top_n_words[-1][0]:
			top_n_words[-1] = (common, i)
			top_n_words.sort(key=lambda x: x[0], reverse = True)
	return top_n_words

####### test #######
n = 10
while True:
	index = random.randint(0,len(CUI1_list)-1)
	CUI1_string = CUI1_list[index]
	print("randomly selected CUI1 string: '%s'" % CUI1_string)
	top_n_words = find_similar(CUI1_string,CUI2_list,n)
	print('top %i' % n, ' similar phrases in CUI2_list are:')
	for i in top_n_words:
		print(i)
	print('The actual isa relationships are:')
	for i in rela_dict[CUI1_string]:
		print(i)
	print('\nso false relations could be:')
	for i in top_n_words:
		if(i[1] not in rela_dict[CUI1_string]):
			print(i[1])
	print("\n")
	a = input()
#####################

n = 6

data_N = 1000

cui1_list = []
cui2_list = []

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

for i in range(data_N):
	perc = int(i/data_N*50)
	bar.update(perc)
	# find similar to CUI1
	index = random.randint(0,len(CUI1_list)-1)
	CUI1_string = CUI1_list[index]
	top_n_words = find_similar(CUI1_string,CUI2_list,n)
	
	false_concepts_pool = []
	for i in top_n_words:
		if(i[1] not in rela_dict[CUI1_string]):
			false_concepts_pool.append(i[1])
	if(len(false_concepts_pool)):
		cui1_list.append(CUI1_string)
		cui2_list.append(random.choice(false_concepts_pool))

for i in range(data_N):
	perc = int(50+i/data_N*50)
	bar.update(perc)
	# find similar to CUI2
	index = random.randint(0,len(CUI2_list)-1)
	CUI2_string = CUI2_list[index]
	top_n_words = find_similar(CUI2_string,CUI1_list,n)
	
	false_concepts_pool = []
	for i in top_n_words:
		if(CUI2_string not in rela_dict[i[1]]):
			false_concepts_pool.append(i[1])
	if(len(false_concepts_pool)):
		cui1_list.append(random.choice(false_concepts_pool))
		cui2_list.append(CUI2_string)

bar.finish()

df2 = pd.DataFrame(np.array([cui1_list,cui2_list]).T,
                   columns=['CUI1', 'CUI2'])

df2.to_csv('non_isa.csv')



