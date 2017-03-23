from sklearn.cluster import KMeans
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
with open('data_0_0_0.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    data = list(reader)

#print data[10]

counter=1
final_list=[]
for x in data:
	l=[]
	l.append("cluster_"+str(counter))
	l.append(x[0])
	#print "intermediate:",l
	#print "x:",x
	for y in data:
		try:
			#print "y:",y
			if x[2]==y[2]:
				ratio=fuzz.ratio(x[1], y[1])
				partial_ratio=fuzz.partial_ratio(x[1], y[1])
				token_set_ratio=fuzz.token_set_ratio(x[1], y[1])
				if(ratio>=75 and partial_ratio>=75 and token_set_ratio>=75):
					l.append(y[0])
					data.remove(y)
			#print "l:",l
		except IndexError:
			print "index error"	
	counter+=1
	print counter					
	final_list.append(l)		
	#data.remove(x)

print final_list



