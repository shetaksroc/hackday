import numpy as np
import csv
import json,sys
import re
import utils
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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


def clustering(clustered_lists):
	for key, value in clustered_lists.iteritems():
		score_list=[]
		first_sku_index = 0
		updatedValues = value
		while (first_sku_index < len(updatedValues)):#len(updatedValues)):
			sec_sku_index = first_sku_index + 1
			first_sku = updatedValues[first_sku_index]
			while (sec_sku_index < len(updatedValues)):#len(updatedValues)):
				sec_sku = updatedValues[sec_sku_index]

				ratio=fuzz.ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
				partial_ratio=fuzz.partial_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
				token_set_ratio=fuzz.token_set_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])

				if(ratio>90 and partial_ratio>90 and token_set_ratio>90):
					score_list.append([first_sku,sec_sku,first_sku[-1]["cluster_id"]])
					#print [first_sku,sec_sku,first_sku[-1]["cluster_id"]],"\n\n"
					try:
						#updatedValues.remove(first_sku)
						updatedValues.remove(sec_sku)
					except ValueError:
						pass	
				sec_sku_index+=1
			try:
				updatedValues.remove(first_sku)
			except ValueError:
				pass	
			first_sku_index+=1			
	return score_list 			

def trimedSize(size):
	size=size.replace("\"","").strip()
	size=size.replace("\'","").strip()
	return size

def compareSize(size1, size2):
	size1=trimedSize(size1)
	size2=trimedSize(size2)

	return size1==size2

def clustering_old(clustered_lists):
	cluster_map={}
	size_map={}
	for key, value in clustered_lists.iteritems():
		score_list=[]
		
		first_sku_index = 0

		updatedValues = value
		while (first_sku_index < len(updatedValues)):#len(updatedValues)):
			sec_sku_index = first_sku_index + 1
			first_sku = updatedValues[first_sku_index]
			size = str(first_sku[2]+"_"+trimedSize(first_sku[-1]['size']))

			#key=str(first_sku[-1]['cluster_id'])
			keyVal=str(first_sku[2]+"_"+first_sku[-1]['cluster_id'])
			first_sku_size = first_sku[-1]['size']
			#print keyVal,"\t\t_",trimedSize(first_sku_size),"_",first_sku[0]
			#print 'first_sku is added : ',key,'\t\t : ',first_sku[0]

			if(size in size_map):
				existing_row=size_map.get(size)
				existing_row.append(first_sku)
				size_map[size]=existing_row
				print keyVal,' Already added first_sku is ',first_sku[0]
			else:
				new_list=[]
				new_list.append(first_sku)
				size_map[size]=new_list
				print keyVal,' Added first_sku is ',first_sku[0]
			
			while (sec_sku_index < len(updatedValues)):#len(updatedValues)):
				sec_sku = updatedValues[sec_sku_index]
				
				sec_sku_size = sec_sku[-1]['size']
				
				if(compareSize(first_sku_size, sec_sku_size) == 0):
					print keyVal,"\t\t_ matched ",trimedSize(first_sku_size)," Vs ",trimedSize(sec_sku_size),first_sku[0],' == ',sec_sku[0]
					try:
						#updatedValues.remove(first_sku)
						existing_row=size_map.get(size)
						existing_row.append(sec_sku)
						size_map[size]=existing_row
						#updatedValues.remove(sec_sku)
					except ValueError:
						pass	
					#cluster_map[first_sku[-1]['cluster_id']]=sec_sku
				else:
					print keyVal," with NO Match in size \t\t_",trimedSize(first_sku_size)," Vs ",trimedSize(sec_sku_size),first_sku[0],' == ',sec_sku[0]
					if(size in size_map):
						existing_row=size_map.get(size)
						existing_row.append(sec_sku)
						size_map[size]=existing_row
					else:
						new_list=[]
						new_list.append(sec_sku)
						size_map[size]=new_list
				#print 'Second Sku is added : ',key,'\t\t : ',first_sku[0]

				try:
					updatedValues.remove(sec_sku)
				except ValueError:
					pass	
				sec_sku_index+=1
			try:
				updatedValues.remove(first_sku)
			except ValueError:
				pass	
			first_sku_index+=1			
	return size_map 			



if __name__== "__main__":
	datalist=loadDataFromJson()
	#print datalist
	distinct_attributes=createDistinctAttributes(datalist)
	key_map = dict()
	clustered_lists=getDistinctLists(datalist)
	size_occurences=getSizeOccurences(clustered_lists)
	#clustered = clustering(clustered_lists)
	clustered = clustering_old(clustered_lists)
	#print clustered

	#	resultMap = {}
#	for skus in clustered:
#		for sku in skus:
#			print "Sku : ",sku
#			#print sku[5]['cluster_id']
#			print "ClusterId : ",sku[-1]['cluster_id']
#			clusterId = sku[-1]['cluster_id']
#			if(clusterId in resultMap):
#				existing_row=resultMap.get(clusterId)
#				existing_row.append(sku)
#				resultMap[clusterId]=existing_row
#			else:
#				new_list=[]
#				new_list.append(sku)
#				resultMap[clusterId]=new_list
#
#
#	for key, value in resultMap.iteritems():
#		print len(value),"\t\t",key
 


	
	#print clustering(clustered_lists)

	#clustered = clustering(clustered_lists)
	#for key, value in clustered.iteritems():
	#	print len(value),"\t\t",key
 

	#for key, value in size_occurences.iteritems():
		#print len(value),"\t\t",key





