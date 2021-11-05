import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import linecache
import sys


class DBPoint:
    def __init__(self, location):
        # Coordinates of the point, as a list
        self.location = location
        # Dimmension of the point (how many coodinates are associated with it)
        self.dim = len(location)
        # DBSCAN type for the point can be core [2], boundry [1], or outlier [0]
        self.type = None
        # The cluster identifier for the point, as an int
        self.cluster = None
        # Boolean T/F for if the point has been visited
        self.visited = False
        # Number of points in the cluter
        self.numNeighbors = 0
        # List of DBPoints contained in this points cluster
        self.neighbors = []

    def __repr__(self):
        return f'DBPoint: {self.location} (dim: {self.dim}); type: {self.type}; cluster: {self.cluster}; visited: {self.visited}; numNeighbors: {self.numNeighbors}; neighbors: not shown'

def exitHelpMessage(error = None):
    if error is not None: print(error)
    print('USAGE: python dbscan <Filename> <epsilon> <NumPoints>')
    print('- <Filename> is the name of the CSV file containing the input dataset.')
    print('- <epsilon> is the Epsilon (ε) parameter of the DBSCAN algorithm: \n\
            the radius within which DBSCAN shall search for points.')
    print('- <NumPoint> is the minimal number of points within the <epsilon> \n\
             distance from a given point to continue building the cluster')
    exit(-1)

def handleCommandLineParams(arguments):
    if len(arguments) == 4:
        fileName = arguments[1]
        try: epsilon = int(arguments[2])
        except: exitHelpMessage("epsilon argument is not int")
        try: numPoints = int(arguments[3])
        except: exitHelpMessage("NumPoint argument is not int")
    else: exitHelpMessage("Argument count incorrect")
    return fileName, epsilon, numPoints

def readData(fileName, dropcols = []):
    try: df = pd.read_csv(fileName, skiprows = 1, header = None)
    except Exception as e: exit(f"ERROR ON {fileName}: {e}")
    header = linecache.getline(fileName, 1).strip().split(",")
    # Drop columns for which the header has a value of '0'
    for i, col in enumerate(header):
        if col == '0': dropcols.append(i)
    df = df.drop(dropcols, axis=1)
    return df

def buildPointList(data, VERBOSE):
    listOfDBPoints= []
    # This is a slow operation, improve if effeciency is a concern
    for point in data.itertuples():
        coordinates = list(point)
        P = DBPoint(coordinates[1:])
        listOfDBPoints.append(P)
    if VERBOSE:
        for point in listOfDBPoints: print(point)
    return listOfDBPoints

def DBSCAN(listOfDBPoints, epsilon, numPoints, VERBOSE):
    # Now we loop through each point one by one
    # Update the point based on the number of points within its epsilon radius
    # Update further if numPoints is large enough, expand that cluster
    
    for point in listOfDBPoints:
        # If we have visited this point already don't check it again
        if point.visited: continue
        for point2 in listOfDBPoints:
            # Check if the point is in range
            point2InRange = pointInEpsilon(point, point2, epsilon)

            # If it is in range, append it to the the first points neighbors
            if point2InRange: 
                if VERBOSE > 1: print(f"FOUND {point2.location} in range of {point.location}")
                point.neighbors.append(point2)
                point.numNeighbors += 1

        #Mark the point as visited
        point.visited = True
        # If it has enough neighbors it is a core point
        if point.numNeighbors >= numPoints: point.type = 2
            

    # We now have all points which are core, each in their own cluster
    curCluster = 0
    for point in listOfDBPoints:
        if not point.type == 2: continue
        if point.cluster is None: 
            point.cluster = curCluster
            expandCluster(point, listOfDBPoints, curCluster)
            curCluster += 1

    for point in listOfDBPoints:
        if point.type is None:
            if point.cluster is not None: point.type = 1
            else: 
                point.cluster =-1
                point.type = 0


    if VERBOSE: 
        for point in listOfDBPoints: print(point)

    return curCluster

def expandCluster(point, listOfDBPoints, curCluster):
    for pointNeighbor in point.neighbors:
        if pointNeighbor.type == 2 and pointNeighbor.cluster != curCluster:
            pointNeighbor.cluster = curCluster
            expandCluster(pointNeighbor, listOfDBPoints, curCluster)
        elif pointNeighbor.cluster != curCluster: pointNeighbor.cluster = curCluster
        


# TODO Use a different distance calculator
def pointInEpsilon(p1, p2, epsilon):
    for axis in range(p1.dim):
        maxAxis = p1.location[axis] + epsilon 
        minAxis = p1.location[axis] - epsilon 
        if p2.location[axis] > maxAxis or p2.location[axis] < minAxis: return False
    return True


#TODO implement lol
def outputResults(listOfDBPoints, numClusters):
    # 1. Cluster number (name)
    # 2. Coordinates of its centroid.
    # 3. Maximum distance from a point to cluster centroid.
    # 4. minimum distance from a point to cluster centroid.
    # 5. average distance from a point to cluster centroid.
    # 6. Sum of Squared Errors (SSE) for the points in the cluster.
    # 7. *Number of points in the cluster, and then all of the points coordinates printed
    # --- OUTLIER INFO ONLY FOR DBSCAN
    # Total number of outliers, 
    # percentage of the dataset outliers constitute
    # List of outliers
    for cluster in range(numClusters):
        pass
       

if __name__ == "__main__":
    TESTING = True
    VERBOSE = 0
    if TESTING:
        fileName = "input_files/iris.csv"
        epsilon = 5
        numPoints = 5
    else: fileName, epsilon, numPoints = handleCommandLineParams(sys.argv)
    data = readData(fileName)
    listOfDBPoints = buildPointList(data, VERBOSE)
    DBSCAN(listOfDBPoints, epsilon, numPoints, VERBOSE)

    outputResults(listOfDBPoints, numClusters)
    
    # Hwere we graph... TODO: move to function
    clusters = []
    for point in listOfDBPoints: clusters.append(point.cluster)
    clusters = pd.concat([data, pd.Series(clusters, name="clusters")], axis=1)
    plt.scatter(clusters.iloc[:,0], clusters.iloc[:,1], c=clusters.clusters)
    #plt.scatter(data.iloc[:,0], data.iloc[:,1])
    plt.show()
