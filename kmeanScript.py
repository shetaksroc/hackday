from sklearn.cluster import KMeans
import numpy as np
import csv
with open('data_0_0_0.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    data = list(reader)
#csv = np.genfromtxt ('data_0_0_0.csv', delimiter="^")
#csv= np.array(csv)
print data[0][1]

X = np.array(data)
kmeans = KMeans(n_clusters=50).fit(X)
kmeans.labels_array([1, 2, 3, 5, 6, 7])

with open('test.csv', 'rb') as f:
    reader = csv.reader(f,delimiter='^')
    test = list(reader)

Y = np.array(test)
kmeans.predict(Y)
