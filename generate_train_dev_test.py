import csv
import pandas as pd 
import numpy as np
import random
isa_CUI1_list = []
isa_CUI2_list = []
isa_label_list = []

non_CUI1_list = []
non_CUI2_list = []
non_label_list = []

non_isa_files = 4
positive_data = non_isa_files*2000
for i in range(1,1+non_isa_files):
	with open('non_isa_'+str(i)+'.csv', newline='') as f:
		reader = csv.reader(f, delimiter=',')
		row1 = next(reader)
		for row in reader:
			non_CUI1_list.append(row[1])
			non_CUI2_list.append(row[2])
			non_label_list.append(0)

with open('isa.csv', newline='') as f:
		reader = csv.reader(f, delimiter=',')
		row1 = next(reader)
		all_isa = []
		for row in reader:
			all_isa.append(row)

		for i in range(positive_data):
			n = random.randint(0,len(all_isa)-1)
			isa_CUI1_list.append(all_isa[n][1])
			isa_CUI2_list.append(all_isa[n][2])
			isa_label_list.append(1)

train_CUI1 = non_CUI1_list[:int(0.7*len(non_CUI1_list))]   +isa_CUI1_list[:int(0.7*len(isa_CUI1_list))]
train_CUI2 = non_CUI2_list[:int(0.7*len(non_CUI2_list))]   +isa_CUI2_list[:int(0.7*len(isa_CUI2_list))]
train_label = non_label_list[:int(0.7*len(non_label_list))]+isa_label_list[:int(0.7*len(isa_label_list))]

dev_CUI1 = non_CUI1_list[int(0.7*len(non_CUI1_list)):int(0.9*len(non_CUI1_list))]    +isa_CUI1_list[int(0.7*len(isa_CUI1_list)):int(0.9*len(isa_CUI1_list))]
dev_CUI2 = non_CUI2_list[int(0.7*len(non_CUI2_list)):int(0.9*len(non_CUI2_list))]    +isa_CUI2_list[int(0.7*len(isa_CUI2_list)):int(0.9*len(isa_CUI2_list))]
dev_label = non_label_list[int(0.7*len(non_label_list)):int(0.9*len(non_label_list))]+isa_label_list[int(0.7*len(isa_label_list)):int(0.9*len(isa_label_list))]

test_CUI1 = non_CUI1_list[int(0.9*len(non_CUI1_list)):]   +isa_CUI1_list[int(0.9*len(isa_CUI1_list)):]
test_CUI2 = non_CUI2_list[int(0.9*len(non_CUI2_list)):]   +isa_CUI2_list[int(0.9*len(isa_CUI2_list)):]
test_label = non_label_list[int(0.9*len(non_label_list)):]+isa_label_list[int(0.9*len(isa_label_list)):]

df1 = pd.DataFrame(np.array([train_CUI1,train_CUI2,train_label]).T,
                   columns=['CUI1', 'CUI2', 'label'])


df2 = pd.DataFrame(np.array([dev_CUI1,dev_CUI2,dev_label]).T,
                   columns=['CUI1', 'CUI2', 'label'])

df3 = pd.DataFrame(np.array([test_CUI1,test_CUI2,test_label]).T,
                   columns=['CUI1', 'CUI2', 'label'])

df1.to_csv('train.csv')
df2.to_csv('dev.csv')
df3.to_csv('test.csv')

