import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt

def select_Centroids(data, k):
    X = data.copy()
    data_center = X.mean()
    centroids = [[] for i in range(k)]
    index = euclidean_distances(X, [data_center]).argmax()
    centroids[0] = list(X.iloc[index])
    X = X.drop(index)
    for cluster in range(1, k):
        index = euclidean_distances(X, centroids[:cluster]).sum(axis=1).argmax()
        centroids[cluster] = list(X.iloc[index])
        X = X.drop(index)
    return centroids

def k_means(data, k):
    X = data.copy()
    centroids = select_Centroids(data, k)
    epochs = 1
    while epochs <= 300:
        clusters = euclidean_distances(X, centroids).argmin(axis=1)
        old_centroids = centroids.copy()
        for centroid in range(len(centroids)):
            centroids[centroid] = np.array(X.iloc[clusters == centroid].mean())
        if np.equal(centroids, old_centroids).all():
            break
    return clusters

data = pd.read_csv("resources/datasets/4clusters.csv")

clusters = pd.concat([data, pd.Series(k_means(data, 3), name="clusters")], axis=1)

plt.scatter(clusters.iloc[:,0], clusters.iloc[:,1], c=clusters.clusters)
plt.show()

