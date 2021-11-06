CSC 466 Lab 4 Report: Clustering - README

- Authors
Otakar Andrysek | oandryse@calpoly.edu
Nathan Johnson  | njohns60@calpoly.edu 



- Running the Code
Code was tested in Python 3.9 however any version Python 3.6+ 'should' work.

Standard data science packages such as pandas and numpy are required. 
Also required are pyplot and linecache for graphing and custom input file 
reading, respectively.

All three algorithms are in separate python files and can be run in the command 
line taking several arguments as shown below.

KMEANS
USAGE: python kmeans.py <Filename> <k>
- <Filename> is the name of the CSV file containing the input dataset.
- <k> is the number of clusters the program has to produce.

HCLUSTERING
USAGE: python hclustering.py <Filename> <k>
- <Filename> is the name of the CSV file containing the input dataset.
- [<threshold>] is the optional number of clusters the program has to produce.

DBSCAN
USAGE: python dbscan <Filename> <epsilon> <NumPoints>
- <Filename> is the name of the CSV file containing the input dataset.
- <epsilon> is the Epsilon (ε) parameter of the DBSCAN algorithm: 
            the radius within which DBSCAN shall search for points.
- <NumPoint> is the minimal number of points within the <epsilon> 
             distance from a given point to continue building the cluster



- Introduction (Can be read in lab report)

In Lab 4 we implemented three different algorithms 
(K-means, Hierarchical Clustering, and DBSCAN) to perform unsupervised learning 
(clustering). These algorithms were then run against six datasets to calibrate 
ideal hyperparameters for each dataset and to discover strengths and weaknesses 
of each of the algorithms.



- Algorithm Design (Can be read in lab report)

For the K-means clustering algorithm we decided to mainly stick to the simpler 
implementation. We did implement the initial selection of centroids that was 
discussed in class, where each next centroid is the furthest point from all 
other centroids. We have two stopping conditions: when the new centroid is equal
to the previous centroid or after 500 iterations. We are using euclidean
distance as the distance measure, the centroids are computed as the means of 
their respective cluster, we didn’t apply any transformations to the data, 
and did not address outliers. 

As with K-means there were also some choices we had when implementing our 
Agglomerative Hierarchical Clustering Algorithm. Firstly, we decided to keep 
using euclidean distance as our distance measure. To calculate the distance 
between clusters we decided to use complete linkage. Complete linkage is very 
interesting because it computes the distance between clusters as the furthest 
distance between all points of the two clusters. This causes the clusters that 
are created to be tighter or closer together than a single or average link. We 
also decided to have our dendrogram in JSON format rather than XML format. 

Our DBSCAN implementation was straightforward, mostly relying on a custom data 
structure, DBPoint. Upon reading the dataset all points are pushed into a list 
of DBPoints. This structure among other attributes holds the cluster 
information, point type, and neighbor DBpoint references. All distance values 
are Euclidean distances and the list of points is updated, once for neighborhood
discovery, again for cluster formation, and finally for point type selection. 
Cluster and outlier information is outputted to the console.