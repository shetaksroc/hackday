#!/usr/bin/env python
from __future__ import print_function
import threading
import time
from sklearn.cluster import KMeans
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import thread

def callable(x):
        score_list=[]
        for y in data:
            if(len(x)!=0 and len(y)!=0):
                print (x,y)
                ratio=fuzz.ratio(x[1], y[1])
                partial_ratio=fuzz.partial_ratio(x[1], y[1])
                token_set_ratio=fuzz.token_set_ratio(x[1], y[1])
                score_list.append([x,y,ratio,partial_ratio,token_set_ratio])
        with open("score_output2.csv",'wb') as resultFile:
                wr=csv.writer(resultFile, dialect='excel')
                wr.writerow(score_list)

with open('data_0_0_0.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    data = list(reader)
for x in data:                                     # Four times...
    #mythread = MyThread(name = "Thread-{}".format(x))  # ...Instantiate a thread and pass a unique ID to it
    #mythread.start()                                   # ...Start the thread
    thread.start_new_thread( callable, (x, ) )
           