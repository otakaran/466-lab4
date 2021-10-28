import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import euclidean_distances
import sklearn.cluster 

"""
def k_means(data):
    domains = [None] * len(data.columns)
    for column in range(len(data.columns)):
        domains[column] = (data.iloc[:,column].min(), data.iloc[:,column].max())
    k = 10
    centroids = [[] for i in range(k):
    for column in range(len(centroids)):
        centroids[column] = random.randint(int(domains[column][0]), int(domains[column][1]))
    print(centroids)
    epochs = 1
    while epochs <= 1000:
        clusters = [[] for j in range(k)]
        for row in range(len(data)):
            dist_big = 0
            big_cluster = None
            for cluster in range(len(centroids)):
                print(centroids[cluster])
                dist = euclidean_distances(data.iloc[row], centroids[cluster])
                if dist > dist_big:
                    dist_big = dist
                    big_cluster = cluster
            clusters[big_cluster].append(row)
        old_clusters = clusters
        for cluster in range(len(clusters)):
            clusters[cluster] = data.iloc[old_clusters].mean()
        if (clusters == old_clusters).all():
            break
    print(clusters)
"""

data = pd.read_csv("filledData.csv")
y = data[1]
X = data[-1]
print(X)
