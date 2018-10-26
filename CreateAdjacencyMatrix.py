import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib import pyplot, patches
import seaborn as sns
import networkx as nx

def euclidean_distance(u,v):
    dist = 0.0
    for i in range(len(u)):
        dist = dist + ((u[i] - v[i])**2)
    dist = dist**0.5
    return dist

def createAdjacencyMatrix(vectors):
    adjacencyMatrix = np.ones((len(vectors), len(vectors)))
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            adjacencyMatrix[i][j] = euclidean_distance(vectors[i], vectors[j])
    return adjacencyMatrix

def generateInputVectors(ndim, n, min, max):
    labels = ['b', 'g', 'c', 'm', 'y', 'k']
    tags = []
    vectors = np.random.rand(1,ndim)
    for i in range(n):
        a = random.randint(min,max)
        vector = np.random.rand(1,ndim) + a
        tags.append(labels[a % len(labels)])
        vectors = np.concatenate((vectors, vector))
    vectors = vectors[1:len(vectors)]
    return (vectors, tags)

def plot1D(data, index, labels):
    val = 0
    for i in range(len(data[0])):
        plt.plot(data[i][0], val, 'o' + labels[i])
    plt.plot(data[index][0], val, 'rp')
    plt.show()

def plot2D(data, index, labels):
    maxVal = max(data[0])
    init = (0, maxVal)
    for i in range(len(data[0])):
        a = random.random() * (math.pi/2)
        x = getCoordinates(init, data[0][i], a)[0]
        y = getCoordinates(init, data[0][i], a)[1]
        plt.plot(x, y, 'o' + labels[i])
    plt.plot(init[0], init[1], 'rp')
    plt.show()

def getCoordinates(init, distance, rad):
    x = distance*math.cos(rad)
    y = distance * math.sin(rad)
    return (init[0]+x, init[1]+y)

def main():
    vectors, tags = generateInputVectors(10,300, 0, 9)
    #vectors = [[1,1,1], [1,1,1], [2,2,2], [2,2,2], [3,3,3], [3,3,3]]
    a = createAdjacencyMatrix(vectors)
    matrix = sns.clustermap(a)
    plt.show()
    plt.figure()
    data = matrix.data2d
    plot1D(data, 0, tags)
    plot2D(data, 0, tags)
    exit(0)
    fig = pyplot.figure(figsize=(5,5))
    #pyplot.imshow(a, cmap = "Greys", interpolation="none")
    #pyplot.show()
    Graph = nx.from_numpy_matrix(a)
    pos = nx.spring_layout (Graph, pos = nx.spring_layout(Graph, k=0.3*1/np.sqrt(len(Graph.nodes())), iterations=20))
    color_map = []
    edge_colors = []
    weights = []
    color_list = ['red', 'blue', 'green', 'yellow', 'orange', 'black', 'purple']
    j = 0
    for node in Graph:
        color_map.append(color_list[int(j/10)])
        for i in range(30):
            edge_colors.append(color_list[int(j/10)])
            weights.append(0)
        j = j + 1

    nx.draw(Graph, pos = pos, node_color = color_map, edge_color = edge_colors, width=weights, with_labels=False, node_size=7)
    plt.show()
if __name__ == '__main__':
    main()
