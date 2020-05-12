import mysql.connector
import random 

mydb = mysql.connector.connect(
	host='127.0.0.1', 
	user= 'root', 			# change to your user name,
	password = 'mck19970824!',		# change to your password
	database='umls',	# change to your database name
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor(buffered=True)

RELA = 'disease_has_finding'

mycursor.execute("SELECT * FROM MRREL WHERE RELA=%s;", (RELA,))

isa_data_all = mycursor.fetchall()
random.shuffle(isa_data_all)
for isa_data in isa_data_all:
	CUI1 = isa_data[0]
	CUI2 = isa_data[4]

	# print("\ndisplay the relationship in English:")
	mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI1,))
	CUI1_string = mycursor.fetchall()
	mycursor.execute("SELECT str from mrconso b WHERE b.cui=%s AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';",(CUI2,))
	CUI2_string = mycursor.fetchall()
	print("%s %s %s" % (CUI2_string[0][0], RELA, CUI1_string[0][0]))
	a = input()

####### For Concept 1: #######

print('\nFind all atoms of a UMLS concept')
mycursor.execute("SELECT * FROM mrconso WHERE cui=%s;",(CUI1,))
atom_data = mycursor.fetchall()
for x in atom_data:
	print(x)

print('\nFind all source definitions associated with a UMLS concept')
mycursor.execute("SELECT * FROM mrdef WHERE cui = %s;",(CUI1,))
def_data = mycursor.fetchall()
for x in def_data:
	print(x)

# print(Find all source contexts associated with a UMLS concept.)
# mycursor.execute("SELECT * FROM mrhier WHERE cui = %s;",(CUI1,))
# src_data = mycursor.fetchall()
# for x in src_data:
# 	print(x)

print('\nFind all attributes for a UMLS concept.')
mycursor.execute("SELECT * FROM mrsat WHERE cui = %s AND stype = 'CUI';", (CUI1,))
attr_data = mycursor.fetchall()
for x in attr_data:
	print(x)

print('\nFind all semantic types for a UMLS concept.')
mycursor.execute("SELECT * FROM mrsty WHERE cui = %s;", (CUI1,))
seman_data = mycursor.fetchall()
for x in seman_data:
	print(x)
print('\nFind all relationships for a UMLS concept.')
mycursor.execute("SELECT * FROM mrrel WHERE cui1 = %s;", (CUI1,))
rela_data = mycursor.fetchall()
for x in rela_data:
	print(x)

print('\nFind all inverse relationships for a UMLS concept.')
mycursor.execute("SELECT * FROM mrrel WHERE cui2 = %s; AND stype2 = 'CUI';", (CUI1,))
inv_rela_data = mycursor.fetchall()
for x in inv_rela_data:
	print(x)

# print('\nFind all relationships for a concept and the preferred (English) name of the CUI2.')
# mycursor.execute("SELECT a.cui1, a.cui2, b.str FROM mrrel a, mrconso b WHERE a.cui1 = %s AND a.stype1 = 'CUI' AND a.cui2 = b.cui AND b.ts = 'P' AND b.stt = 'PF' AND b.ispref = 'Y' AND b.lat = 'ENG';", (CUI1,))
# inv_rela_data = mycursor.fetchall()
# for x in inv_rela_data:
# 	print(x)

