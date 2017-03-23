import numpy as np
import csv
import json,sys
import re

def loadDataFromJson():
	txt = open(sys.argv[1]);
	data_in_string_format=txt.read()
	data_list=json.loads(data_in_string_format)
	final_list=[]
	for row in data_list:
		row_list=[]
		for column in row:
			column_value=str(row[column])
			replaced = re.sub('\(.*\)', '', column_value)
			replaced = re.sub('\\\\', '', replaced)
			row_list.append(replaced)
		final_list.append(row_list)
	return final_list		
#print final_list

def createDistinctAttributes(final_list):
	brand=set()
	merch_l1=set()
	merch_l2=set()
	merch_l3=set()
	distinct_attributes=dict()
	for row in final_list:
		brand.add(row[2])
		merch_l1.add(row[4])
		merch_l2.add(row[5])
		merch_l3.add(row[6])
	distinct_attributes['brand']=brand
	distinct_attributes['merch_l1']=merch_l1
	distinct_attributes['merch_l2']=merch_l2
	distinct_attributes['merch_l3']=merch_l3
	distinct_list=list()
	distinct_list.append(brand)
	distinct_list.append(merch_l1)
	distinct_list.append(merch_l2)
	distinct_list.append(merch_l3)
	return distinct_list

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
	return final_map

#getDistinctLists(final_list)		

if __name__== "__main__":
	datalist=loadDataFromJson()
	distinct_attributes=createDistinctAttributes(datalist)
	clustered_lists=getDistinctLists(datalist)
	print clustered_lists




