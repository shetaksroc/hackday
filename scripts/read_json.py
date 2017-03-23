import numpy as np
import csv
import json,sys
txt = open(sys.argv[1]);
data_in_string_format=txt.read()
data_list=json.loads(data_in_string_format)
final_list=[]
for row in data_list:
	row_list=[]
	for column in row:
		row_list.append(row[column])
	final_list.append(row_list)	
print final_list
print len(final_list) 
