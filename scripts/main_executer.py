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
	clusterMap = {}
	for key, value in clustered_lists.iteritems():
		score_list=[]
		first_sku_index = 0
		updatedValues = value
		
		
		while (first_sku_index < len(updatedValues)):#len(updatedValues)):
			addedskus=[]
			sec_sku_index = first_sku_index + 1

			first_sku = updatedValues[first_sku_index]
			addedskus.append(first_sku[0])
			while (sec_sku_index < len(updatedValues)):#len(updatedValues)):
				sec_sku = updatedValues[sec_sku_index]

				ratio=fuzz.ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
				partial_ratio=fuzz.partial_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
				token_set_ratio=fuzz.token_set_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])

				if(ratio>90 and partial_ratio>90 and token_set_ratio>90):
					#score_list.append([first_sku,sec_sku,first_sku[-1]["cluster_id"]])
					addedskus.append(sec_sku[0])
					#print [first_sku,sec_sku,first_sku[-1]["cluster_id"]],"\n\n"
					try:
						#updatedValues.remove(first_sku)
						value.remove(sec_sku)
					except ValueError:
						pass	
				sec_sku_index+=1
			key = first_sku[2]+"_"+first_sku[-1]['size'] # brand_cluster_1
			if(key in clusterMap):
				existing_row=clusterMap.get(key)
				existing_row.append(addedskus)
				clusterMap[key]=existing_row
				#print keyVal,' Already added first_sku is ',first_sku[0]
			else:
				clusterMap[key]=addedskus	
			
			try:
				value.remove(first_sku)
			except ValueError:
				pass	
			
			first_sku_index+=1			
	#return score_list 			
	return clusterMap

def trimedSize(size):
	size=size.replace("\"","").strip()
	size=size.replace("\'","").strip()
	return size

def getSortedSize(size):
	nos = size.lower().split('x')
	newNos = []
	for i in nos:
		newNos.append(i.strip())
	return sorted(newNos)

def compareSize(size1, size2, sort):
	size1=trimedSize(size1)
	size2=trimedSize(size2)

	if(sort):
		size1=getSortedSize(size1)
		size2=getSortedSize(size2)
		if(cmp(size1, size2)==0):
			return True
		else:
			return False

	return size1 == size2

def cluster_efficient(clustered_lists):
	clusteredSkusMap = {}
	for cluserId, skusList in clustered_lists.iteritems():
		alreadyAddedSkus = []
		clusteredSkus = []
		#print skusList
		i = 0
		while(i < len(skusList)):
			first_sku = skusList[i]
			if(i not in alreadyAddedSkus):
				alreadyAddedSkus.append(i)
				clusteredSkus.append(skusList[i])
				skusList.remove(skusList[i])
				j = i + 1
				while( j < len(skusList)):
					if(j not in alreadyAddedSkus):
						#print skusList
						first_sku_size=skusList[i][-1]['size']
						sec_sku_size=skusList[j][-1]['size']
						## Here we need to say the deciding logic
						## we shall make more generic
						if(compareSize(first_sku_size, sec_sku_size) == 0):
							alreadyAddedSkus.append(j)
							clusteredSkus.append(skusList[j])
							skusList.remove(skusList[j])
					j+=1
			#removed the cluster_id
			key = first_sku[2]+"_"+cluserId # brand_cluster_1
			if(key in clusteredSkusMap):
				existing_row=clusteredSkusMap.get(key)
				existing_row.append(clusteredSkus)
				clusteredSkusMap[key]=existing_row
				#print keyVal,' Already added first_sku is ',first_sku[0]
			else:
				new_list=[]
				new_list.append(clusteredSkus)
				clusteredSkusMap[key]=new_list
				#print keyVal,' Added first_sku is ',first_sku[0]
			i+=1

	return clusteredSkusMap
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
				#print keyVal,' Already added first_sku is ',first_sku[0]
			else:
				new_list=[]
				new_list.append(first_sku)
				size_map[size]=new_list
				#print keyVal,' Added first_sku is ',first_sku[0]
			
			while (sec_sku_index < len(updatedValues)):#len(updatedValues)):
				sec_sku = updatedValues[sec_sku_index]
				
				sec_sku_size = sec_sku[-1]['size']
				
				if(compareSize(first_sku_size, sec_sku_size) == 0):
					#print keyVal,"\t\t_ matched ",trimedSize(first_sku_size)," Vs ",trimedSize(sec_sku_size),first_sku[0],' == ',sec_sku[0]
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
					#print keyVal," with NO Match in size \t\t_",trimedSize(first_sku_size)," Vs ",trimedSize(sec_sku_size),first_sku[0],' == ',sec_sku[0]
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

def addToClusterMap(clusterMap, first_sku):
	key = first_sku[2]+"_"+first_sku[-1]['size'] # brand_cluster_1
	if(key in clusterMap):
		existing_skus=clusterMap.get(key)
		existing_skus.append(first_sku)
		clusterMap[key]=existing_skus
		#print keyVal,' Already added first_sku is ',first_sku[0]
	else:
		skusList=[]
		skusList.append(first_sku)
		clusterMap[key]=skusList
	return clusterMap	
	

def clustering_modified_final(clustered_lists):
	clusterMap = {}
	brandChecks = ['trademark fine art','national marker']
	NM = 'national marker'
	for key, value in clustered_lists.iteritems():
		score_list=[]
		
		for first_sku in value:
			addedskus=[]
			unclusterskus=[]
			addedskus.append(first_sku[0])
			for sec_sku in list(value):
				if(first_sku[0] != sec_sku[0]):
					ratio=fuzz.ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
					partial_ratio=fuzz.partial_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
					token_set_ratio=fuzz.token_set_ratio(first_sku[-1]['size'], sec_sku[-1]['size'])
					#if( first_sku[2] in brandChecks):
					#if(ratio>90 and partial_ratio>90 and token_set_ratio>90):
						#score_list.append([first_sku,sec_sku,first_sku[-1]["cluster_id"]])
					sort = False
					if(NM in first_sku[2].lower()):
						sort = True
					if(first_sku[-1]['size'] is None or sec_sku[-1]['size'] is None):
						addedskus.append(sec_sku[0])
						try:
							#updatedValues.remove(first_sku)
							value.remove(sec_sku)
						except ValueError:
							pass

					elif(compareSize(first_sku[-1]['size'], sec_sku[-1]['size'], sort)):
						addedskus.append(sec_sku[0])
						#price_match=checkPriceLogic(float(first_sku[3]),float(sec_sku[3]))
						#if(price_match is True):
						#	addedskus.append(sec_sku[0])
						#	try:
								#updatedValues.remove(first_sku)
						#		value.remove(sec_sku)
						#	except ValueError:
						#		pass
						#else:		
							#unclusterskus.append(sec_sku[0])
						try:
							#updatedValues.remove(first_sku)
							value.remove(sec_sku)
						except ValueError:
							pass
					#print [first_sku,sec_sku,first_sku[-1]["cluster_id"]],"\n\n"
					
						
							
			
#			unclustered_key = "unclustered" # brand_cluster_1
#			
#			if(unclustered_key in clusterMap):
#				existing_row=clusterMap.get(unclustered_key)
#				existing_row.append(unclusterskus)
#				clusterMap[unclustered_key]=existing_row
#				#print keyVal,' Already added first_sku is ',first_sku[0]
#			else:
#				clusterMap[unclustered_key]=unclusterskus		
#
			key = first_sku[2]+"_"+first_sku[-1]['size'] # brand_cluster_1
			
			if(key in clusterMap):
				existing_row=clusterMap.get(key)
				existing_row.extend(addedskus)
				clusterMap[key]=existing_row
				#print keyVal,' Already added first_sku is ',first_sku[0]
			else:
				
				clusterMap[key]=addedskus	
			
			try:
				value.remove(first_sku)
			except ValueError:
				pass				 			
	return clusterMap

def checkPriceLogic(price1,price2):
	if(price1 is None or price2 is  None):
		return False
	elif price1>price2:
		return price1<(1.5* price2)
	elif(price1>price2):
		return price2<(1.5* price1)
	elif(price1==price2):
		return True
	else:
		return False				

def getClusterSkuPair(final_output):
	cluster=1
	sku_cluster=[]
	for key, value in final_output.iteritems():
		for each_sku in value:
			sku_cluster.append("cluster"+str(cluster)+":"+each_sku)
		cluster+=1
	return sku_cluster		

def createJson(cluster_sku):
	output = []
	for entry in cluster_sku:
		data = {}
		data['SKU'] = int(entry.split(":")[1])
		data['Cluster_ID'] = entry.split(":")[0]
		output.append(data)
	json_data = json.dumps(output)
	return json_data	

def writeToFile(filename,jsonoutput):
	with open(filename, 'wb') as f:
		f.write(jsonoutput)
    	


if __name__== "__main__":
	datalist=loadDataFromJson()
	#print datalist
	distinct_attributes=createDistinctAttributes(datalist)
	key_map = dict()
	#this is a dictionary
	clustered_lists=getDistinctLists(datalist)
	#for key, value in clustered_lists.iteritems():
	# 	print len(value),"\t\t",key
	size_occurences=getSizeOccurences(clustered_lists)
	# for key, value in size_occurences.iteritems():
	# 	print len(value),"\t\t",key
	clustered = clustering_modified_final(clustered_lists)
	# for key, value in clustered.iteritems():
	# 	print len(value),"\t\t",key
	final_output=dict()
	for key, value in clustered.iteritems():
		#print "key",key
		#print "value",value	
		if(len(value)>13):
			brand=key.split('_')[0]
		else:
			brand="unclustered"		
		
		if(brand in final_output):
			existing_row=final_output.get(brand)
			existing_row.extend(value)	
			final_output[brand]=existing_row
					
			#print keyVal,' Already added first_sku is ',first_sku[0]
		else:
			#new_list=[]
			#for each_sku in value:
			#	new_list.append(each_sku)			
			final_output[brand]=value

		#print len(value),"\t\t",key
		#if(('surya_') in key):
		#	print "surya : ",value
		#if(len(value) < 20):
		#	print value
	#print final_output
	final_json=createJson(getClusterSkuPair(final_output))
	writeToFile('output.json',final_json);

	


	#print clustered_lists
	#clustered = cluster_efficient(clustered_lists)
	#print clustered
	#for key, value in clustered.iteritems():
	#	print len(value),"\t\t",key
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





