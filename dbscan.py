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

def DBSCAN(listOfDBPoints, epsilon, numPoints):
    # Now we loop through each point one by one
    # Update the point based on the number of points within its epsilon radius
    # Update further if numPoints is large enough, expand that cluster
    curCluster = 0
    for point in listOfDBPoints:
        # If we have visited this point already don't check it again
        if point.visited: continue
        for point2 in listOfDBPoints:
            # Skip if same point
            if point.location == point2.location: continue

            # Check if the point is in range
            point2InRange = pointInEpsilon(point, point2, epsilon)

            # If it is in range, append it to the the first points neighbors
            if point2InRange: 
                print(f"FOUND {point.location} in range of {point2.location}")
                if point2.cluster is None:
                    point.neighbors.append(point2)
                    point.numNeighbors += 1
                else:
                    point.numNeighbors += 1 # maybe this is wrong?
                    print(f"Could not add that point to cluster {curCluster} because it was already in {point2.cluster}")

        #Mark the point as visited
        point.visited = True

        # Now how do we classify it?
        # If not enough points it is an outlier or possibly boundry
        if point.numNeighbors < numPoints:
            point.type = 0

        # If it has enough it is a core point
        if point.numNeighbors >= numPoints:
            point.type = 2
            point.cluster = curCluster
            # All of its neighbors will be in its cluster (we don't know if they will be core or boundry)
            for coreNeighbor in point.neighbors:
                # Don't explore points that are already visited and labled
                if coreNeighbor.visited and coreNeighbor.cluster is not None: continue
                coreNeighbor.cluster = curCluster
                coreNeighbor = expandCluster(coreNeighbor, listOfDBPoints, curCluster, numPoints)
            # Set up for next cluster
            curCluster += 1
    for point in listOfDBPoints: print(point)

        
def expandCluster(point, listOfDBPoints, curCluster, numPoints):
    for point2 in listOfDBPoints:
        # Skip if same point
        if point.location == point2.location: continue

        # Check if the point is in range
        point2InRange = pointInEpsilon(point, point2, epsilon)

        # If it is in range, append it to the the first points neighbors
        if point2InRange: 
            print(f"FOUND {point.location} in range of {point2.location}")
            point.neighbors.append(point2)
            point.numNeighbors += 1
            
            # if point2.cluster is None:
            #     point.neighbors.append(point2)
            #     point.numNeighbors += 1
            # else:
            #     point.numNeighbors += 1 # maybe this is wrong?
            #     print(f"Could not add that point to cluster {curCluster} because it was already in {point2.cluster}")

    # FOund another core point, expand on it
    if point.numNeighbors >= numPoints:
        point.cluster = curCluster
        point.type = 2
        
        # reccusrive call
        for coreNeighbor in point.neighbors:
            # Don't explore points that are already visited and labled
            if coreNeighbor.visited and coreNeighbor.cluster is not None: continue
            coreNeighbor = expandCluster(coreNeighbor, listOfDBPoints, curCluster, numPoints)
    
    # Else we found a boundry point, do not explore further
    else:
        point.cluster = curCluster
        point.type = 1

    point.visited = True
    return point


def pointInEpsilon(p1, p2, epsilon):
    for axis in range(p1.dim):
        maxAxis = p1.location[axis] + epsilon 
        minAxis = p1.location[axis] - epsilon 
        if p2.location[axis] > maxAxis or p2.location[axis] < minAxis: return False
    return True

if __name__ == "__main__":
    TESTING = True
    VERBOSE = True
    if TESTING:
        fileName = "input_files/4clusters.csv"
        epsilon = 3
        numPoints = 2
    else: fileName, epsilon, numPoints = handleCommandLineParams(sys.argv)
    data = readData(fileName)
    listOfDBPoints = buildPointList(data, VERBOSE)
    DBSCAN(listOfDBPoints, epsilon, numPoints)


    clusters = []
    for point in listOfDBPoints: clusters.append(point.cluster)
    clusters = pd.concat([data, pd.Series(clusters, name="clusters")], axis=1)
    plt.scatter(clusters.iloc[:,0], clusters.iloc[:,1], c=clusters.clusters)
    #plt.show()
