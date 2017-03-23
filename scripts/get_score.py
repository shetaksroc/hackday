from sklearn.cluster import KMeans
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
with open('cluster1.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    data = list(reader)

score_list=[]
for x in data:
	for y in data:
		if(len(x)!=0 and len(y)!=0):
			#print x,y
			ratio=fuzz.ratio(x[1], y[1])
			partial_ratio=fuzz.partial_ratio(x[1], y[1])
			token_set_ratio=fuzz.token_set_ratio(x[1], y[1])
			score_list.append([x,y,ratio,partial_ratio,token_set_ratio])	
	
with open("score_output.csv",'wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerow(score_list)




