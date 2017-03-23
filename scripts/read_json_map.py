import numpy as np
import csv
import json,sys
import re
txt = open(sys.argv[1]);
data_in_string_format=txt.read()
data_list=json.loads(data_in_string_format)
final_list=[]
for row in data_list:
	row_list=[]
	for column in row:
		column_value=str(row[column])
		replaced = re.sub('\(.*\)', '', column_value)
		row_list.append(replaced)
	final_list.append(row_list)	
#print final_list

def createDistinctAttributes(final_list):
	brands=set()
	merch_l1=set()
	merch_l2=set()
	merch_l3=set()
	distinct_attributes=dict()
	for row in final_list:
		brands.add(row[2])
		merch_l1.add(row[4])
		merch_l2.add(row[5])
		merch_l3.add(row[6])
	distinct_attributes['brands']=brands
	distinct_attributes['merch_l1']=merch_l1
	distinct_attributes['merch_l2']=merch_l2
	distinct_attributes['merch_l3']=merch_l3	
	return list(brands,merch_l1,merch_l2,merch_l3)	

#print brands
#print merch_l1
#print merch_l2
#print merch_l3
#print len(final_list) 
def getDistinctLists(data):
	final_map=dict()
	for each_row in data:
		key=str(each_row[2]+"^"+each_row[4]+"^"+each_row[5]+"^"+each_row[6])
		if(key in final_map):
			existing_row=final_map.get(key)
			existing_row.append(each_row)
			final_map[key]=existing_row
		else:
			final_map[key]=each_row
	print len(final_map)

getDistinctLists(final_list)					
