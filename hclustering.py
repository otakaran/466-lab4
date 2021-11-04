import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def distance_matrix(data):
    distances = pd.DataFrame()
    for row in range(len(data)):
        distances[row] = np.sqrt(((data - data.iloc[row]) ** 2).sum(axis=1))
    np.fill_diagonal(distances.values, np.NAN)
    return distances


def agglomerative(data):
    # Initialize Clusters, Leaf Nodes, and Distance Matrix
    clusters = [[x] for x in range(len(data))]
    nodes = {x: {"type": "leaf", "height": 0.0, "data": data.iloc[x].values} for x in range(len(data))}
    distances = distance_matrix(data)

    # Size keeps track of original data size; i is how many new clusters - 1
    size = len(clusters)
    i = 0

    while len(clusters) < 2 * size - 1:
        # Find smallest distance (dist), r = rowIndex, c = colIndex
        r, c, dist = distances.loc[:, distances.min().idxmin()].idxmin(), distances.min().idxmin(), distances.min().min()

        # Create the new clusters and nodes
        clusters.append([r,c])
        if len(clusters) == 2 * size - 2:
            nodes[size + i] = {"type": "root", "height": dist, "nodes": [nodes[r], nodes[c]]}
        else:
            nodes[size + i] = {"type": "node", "height": dist, "nodes": [nodes[r], nodes[c]]}

        # Add the complete link distance for new cluster, and delete old clusters
        distances[size+i] = distances[[r, c]].max(axis=1)
        distances = distances.append(pd.Series(distances[[r, c]].max(axis=1), name=size+i))
        distances = distances.drop([r, c], axis=1)
        distances = distances.drop([r, c])

        i += 1
    return nodes[size * 2 - 2]

# Gets a list where each element is a cluster
def get_clusters(tree, threshold):
    clusters = []
    if tree["height"] < threshold:
      return [tree]
    left = get_clusters(tree["nodes"][0], threshold)
    right = get_clusters(tree["nodes"][1], threshold)
    for cluster in left:
        clusters.append(cluster)
    for cluster in right:
        clusters.append(cluster)
    return clusters  

# Convert individual clusters in dataframe of data with assignments as last column (left)
def get_leaf_nodes(tree, cluster):
    clusters = []
    if tree["type"] == "leaf":
        values = list(tree["data"])
        values.append(cluster)
        return [values]
    left = get_leaf_nodes(tree["nodes"][0], cluster)
    right = get_leaf_nodes(tree["nodes"][1], cluster)
    for cluster in left:
        clusters.append(cluster)
    for cluster in right:
        clusters.append(cluster)
    return clusters


data = pd.read_csv("resources/datasets/4clusters.csv")
threshold = 30

dendrogram = agglomerative(data)
cluster_list = get_clusters(dendrogram, threshold)
assignments = pd.DataFrame()
for cluster in range(len(cluster_list)):
    assignments = assignments.append(get_leaf_nodes(cluster_list[cluster], cluster), ignore_index=True)

plt.scatter(assignments.iloc[:,0], assignments.iloc[:,1], c=assignments.iloc[:,-1])
plt.show()
