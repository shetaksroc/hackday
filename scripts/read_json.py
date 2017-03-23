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
#print final_list

brands=set()
merch_l1=set()
merch_l2=set()
merch_l3=set()
for row in final_list:
	brands.add(row[2])
	merch_l1.add(row[4])
	merch_l2.add(row[5])
	merch_l3.add(row[6])

#print brands
#print merch_l1
#print merch_l2
#print merch_l3
#print len(final_list) 
def getDistinctLists(data):
	final_cluster=[]
	for row1 in data:
		similar_group=[]
		#print "Row1",row1
		if(len(data)==1):
			similar_group.append(row1)
			data.remove(row1)
		for row2 in list(data):
			#print "Row2",row2
			try:
				if(row1[2]==row2[2] and row1[4]==row2[4] and row1[5]==row2[5] and row1[6]==row2[6]):
					similar_group.append(row2)
					data.remove(row2)
			except ValueError:
				pass
		#print similar_group
		print "Data:",data
		try:				
			final_cluster.append(similar_group)
			data.remove(row1)
		except ValueError:
			pass	

	print len(final_cluster)
getDistinctLists(final_list)

#create clusters on brand,merch_l1,merch_l2,merch_l3


				


