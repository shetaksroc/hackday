from sklearn.cluster import KMeans
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
import csv
with open('data_0_0_0.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    data = list(reader)

print len(data)    