import numpy as np
import csv
import json,sys
import re
import utils
def loadDataFromJson():
	txt = open(sys.argv[1]);
	data_in_string_format=txt.read()
	data_list=json.loads(data_in_string_format)
	final_list=[]

	for row in data_list:
		row_list=[]
		attributes={}

		#attributes['size']=utils.getSizes(row['TITLE']).replace("\'","").strip()
		#attributes['size']=attributes['size'].replace("\"","").strip()
		original_title = attributes['original_title']=row['TITLE']
		attributes['original_size']=original_size=utils.getSizes(re.sub('\\\\', '', original_title))
		for column in row:
			column_value=str(row[column])
			replaced = re.sub('\(.*\)', '', column_value)
			replaced = re.sub('\\\\', '', replaced)
			replaced = replaced.replace(",","")
			replaced = replaced.replace("\'","").strip()
			row_list.append(replaced.lower())
		
		title=row_list[1]
		#print "current Title : ",title
		attributes['cluster_id']="dummy_cluster"
		#original_size=utils.getSizes(title)
		attributes['size']=utils.getSizes(title)
		#original_size=attributes['size']
		attributes['size']=attributes['size'].replace("\"","").strip()
		attributes['color']=utils.getColor(title)
		attributes['quantity']=utils.getPackQuantity(title)
		attributes['type']=utils.getProductType(attributes['original_title'],original_size,row_list[2])
		attributes['sub_brand']=""	
		attributes['material']=""
		row_list.append(attributes)	
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

	counter=1
	for each_row in data:
		key=str(each_row[2]+"^"+each_row[4]+"^"+each_row[5]+"^"+each_row[6])
		if(key in final_map):
			existing_row=final_map.get(key)
			each_row[-1]['cluster_id']="cluster_"+key_map[key]
			existing_row.append(each_row)
			final_map[key]=existing_row
		else:
			new_list=[]
			key_map[key] = str(counter)
			each_row[-1]['cluster_id']="cluster_"+key_map[key]
			counter+=1
			new_list.append(each_row)
			final_map[key]=new_list
			existing_row=final_map.get(key)
			
	return final_map

#getDistinctLists(final_list)		

def getSizeOccurences(clustered_lists):
	size_count=dict()
	for key, value in clustered_lists.iteritems():
		for row in value:
			if(row[-1]['size'] in size_count):
				skus_in_size=size_count.get(row[-1]['size'])
				skus_in_size.append(row[0])
				size_count[row[-1]['size']]=skus_in_size
			else:
				new_sku=[]
				new_sku.append(row[0])
				size_count[row[-1]['size']]=new_sku
	return size_count			








if __name__== "__main__":
	datalist=loadDataFromJson()
	print datalist
	distinct_attributes=createDistinctAttributes(datalist)
	key_map = dict()
	clustered_lists=getDistinctLists(datalist)
	size_occurences=getSizeOccurences(clustered_lists)
	#print size_occurences
	#for key, value in size_occurences.iteritems():
		#print len(value),"\t\t",key





