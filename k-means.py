import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import euclidean_distances


def k_means(data, k):
    domains = [None] * len(X.columns)
    for column in range(len(X.columns)):
        domains[column] = (X.iloc[:,column].min(), X.iloc[:,column].max())
    centroids = [[] for i in range(k)]
    for cluster in range(len(centroids)):
        for column in range(len(domains)):
            centroids[cluster].append(data.iloc[random.randint(0, len(X)), column])
    epochs = 1
    while epochs <= 100:
        clusters = [[] for j in range(k)]
        for row in range(len(data)):
            dist_big = 0
            big_cluster = None
            for cluster in range(len(centroids)):
                dist = euclidean_distances(np.array(X.iloc[row]).reshape(1,-1), np.array(centroids[cluster]).reshape(1,-1))
                if dist > dist_big:
                    dist_big = dist
                    big_cluster = cluster
            clusters[big_cluster].append(row)
        old_centroids = centroids
        for centroid in range(len(centroids)):
            centroids[centroid] = np.array(X.iloc[clusters[centroid]].mean())
        if (centroids == old_centroids):
            break

