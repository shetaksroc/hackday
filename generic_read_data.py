import numpy as np
import csv
import sys
with open(sys.argv[1], 'rb') as f:
    reader = csv.reader(f,delimiter=sys.argv[2])
    data = list(reader)

print len(data)    