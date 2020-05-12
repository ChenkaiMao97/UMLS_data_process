import csv
import pandas as pd 
import numpy as np
import random

path = 'relas/'
# names = ['has_manifestation', 'disease_has_finding', 'occurs_after', 'disease_excludes_finding', 'associated_finding_of', 'has_contraindicated_drug' ,'causative_agent_of', 'may_treat', 'associated_with', 'disease_has_associated_anatomic_site','positively_regulates', 'negatively_regulates', 'regulates', 'gene_is_element_in_pathway','gene_product_is_element_in_pathway', 'gene_encodes_gene_product', 'gene_product_plays_role_in_biological_process', 'gene_plays_role_in_process',
# 		  'has_pathological_process', 'has_branch', 'has_temporal_context', 'has_time_aspect', 'related_to',  'cause_of', 'evaluation_of',  'disease_may_have_finding', 'occurs_in',  'analyzes', 'alias_of', 'measures', 'same_as', 'concept_in_subset', 'method_of', 'mapped_to',
# 		 'classified_as', 'disease_mapped_to_gene', 'gene_product_has_associated_anatomy', 'contains', 'includes', 'used_by', 'has_access', 'used_for', 'disease_may_have_cytogenetic_abnormality', 'disease_excludes_abnormal_cell', 'disease_has_abnormal_cell', 'disease_has_normal_cell_origin', 'disease_has_normal_tissue_origin']
# names = ['train', 'dev', 'test']
names = ['has_manifestation', 'disease_has_finding', 'occurs_after', 'disease_excludes_finding', 'associated_finding_of']
# DISEASE concept group: (x13)
# names = ['disease_has_finding','disease_excludes_finding','disease_may_have_finding','disease_has_associated_anatomic_site','disease_mapped_to_gene','disease_may_have_cytogenetic_abnormality','disease_excludes_abnormal_cell','disease_has_abnormal_cell','disease_has_normal_cell_origin','disease_has_normal_tissue_origin']

# REGULATION concept group (x1.5)
# names =['positively_regulates', 'negatively_regulates', 'regulates'] 

# TREATMENT concept group (x5)
# names = ['may_treat', 'has_contraindicated_drug']

# GENE concept group (x8)
# names = ['gene_is_element_in_pathway', 'gene_plays_role_in_process', 'gene_product_is_element_in_pathway', 'gene_encodes_gene_product', 'gene_product_plays_role_in_biological_process', 'gene_product_has_associated_anatomy', 'gene_plays_role_in_process']

# Other concept group (x3)
# names = ['has_pathological_process', 'occurs_after', 'causative_agent_of', 'occurs_in']


nodes = dict()
count = 0

edges_count=0

def add_to_sets(f):
	global count, edges_count
	reader = csv.reader(f, delimiter=',')
	row1 = next(reader)
	for row in reader:
		if row[1] not in nodes.keys():
			nodes[row[1]] = count
			count += 1
		if row[2] not in nodes.keys():
			nodes[row[2]] = count
			count += 1
		# if row[3] == '1' and (nodes[row[1]], nodes[row[2]]) not in edges:
		# 	edges.add((nodes[row[1]], nodes[row[2]]))
		edges_count+=1

def edge_ratio_of_this_relation(f):
	count = 0
	edges_count = 0
	reader = csv.reader(f, delimiter=',')
	row1 = next(reader)
	for row in reader:
		if row[1] not in nodes.keys():
			nodes[row[1]] = count
			count += 1
		if row[2] not in nodes.keys():
			nodes[row[2]] = count
			count += 1
		# if row[3] == '1' and (nodes[row[1]], nodes[row[2]]) not in edges:
		# 	edges.add((nodes[row[1]], nodes[row[2]]))
		edges_count+=1
	return edges_count/count

def shared_ratio_two_files(name1, name2):
	nodes1 = set()
	edge_count1 = 0
	nodes2 = set()
	edge_count2 = 0
	with open(name1+'.csv') as f:
		reader = csv.reader(f, delimiter=',')
		row1 = next(reader)
		for row in reader:
			if row[1] not in nodes1:
				nodes1.add(row[1])
			if row[2] not in nodes1:
				nodes1.add(row[2])
			edge_count1+=1
	with open(name2+'.csv') as f:
		reader = csv.reader(f, delimiter=',')
		row1 = next(reader)
		for row in reader:
			if row[1] not in nodes2:
				nodes2.add(row[1])
			if row[2] not in nodes2:
				nodes2.add(row[2])
			edge_count2+=1
	if(len(nodes1 & nodes2)/min(len(nodes1),len(nodes2))>0):
		print('{:40s} and {:40} ratio1: {:1.3f}		ratio2: {:1.3f}		total edge_ratio: {:1.3f} 		overlap: {:1.3f}'.format(name1, name2, edge_count1/len(nodes1), edge_count2/len(nodes2), (edge_count1 + edge_count2)/len(nodes1 | nodes2),len(nodes1 & nodes2)/min(len(nodes1),len(nodes2))))

# for name in names:
# 	with open(name+'.csv', newline='') as f:
# 		# print(name, ': ', edge_ratio_of_this_relation(f))
# 		add_to_sets(f)
# print(len(nodes.keys()))
# print(edges_count)

for i in range(len(names)-1):
	for j in range(i+1, len(names)):
		shared_ratio_two_files(path+names[i], path+names[j])



