# variable size
from sys import getsizeof
import math

# reading osm
import xml.etree.ElementTree

# plotting
import matplotlib.pyplot as plt
import numpy as np

class Node:
    x = 0;
    y = 0;
    id = 0;

    def __init__(self, x, y, id):
        self.x = float(x)
        self.y = float(y)
        self.id = id

    def normalize(self,bounds):
        self.x = 1/(bounds['maxX']-bounds['minX'])*(self.x-bounds['minX'])*100
        self.y = 1/(bounds['maxY']-bounds['minY'])*(self.y-bounds['minY'])*100

class Edge:
    begin = 0;
    end = 0;

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

def getBoundNodes(nodes):
    maxX = 0
    minX = 0
    maxY = 0
    minY = 0

    for key, node in nodes.items():
        if node.x > maxX or maxX == 0:
            maxX = node.x

        if node.y > maxY or maxY == 0:
            maxY = node.y

        if node.x < minX or minX == 0:
            minX = node.x

        if node.y < minY or minY == 0:
            minY = node.y

    return {'maxX':maxX, 'minX':minX, 'maxY':maxY, 'minY': minY}

def plotGraph(nodes,edges):
    x = []
    y = []

    for key, node in nodes.items():
        x.append(node.x)
        y.append(node.y)

    #plt.plot(x, y, '.')

    for edge in edges:
            node1 = nodes[edge.begin]
            node2 = nodes[edge.end]
            plt.plot([node1.x, node2.x],[node1.y, node2.y])

    plt.show()

def getWays(osm):
    ways = []
    carValues = ['motorway','trunk','primary','secondary','tertiary','unclassified','residential','service','motorway_link','trunk_link','primary_link','secondary_link','tertiary_link','living_street','pedestrian','track','road']

    for way in osm.findall('way'):
        wayNodes = []
        for node in way.iter('nd'):
            wayNodes.append(node.attrib['ref'])

        for tag in way.iter('tag'):
            forCars = tag.attrib['v'] in carValues

            if tag.attrib['k'] == 'highway' and forCars:
                ways.append(wayNodes)

    return ways

def getGraph(fileName):
    nodes = {}

    osm = xml.etree.ElementTree.parse(fileName).getroot()

    for atype in osm.findall('node'):
        newNode = Node(atype.get('lon'),atype.get('lat'),atype.get('id'))
        nodes.update({newNode.id: newNode})

    ways = getWays(osm)

    cleanNodes = {}

    for way in ways:
        for node in way:
            if node in nodes.keys():
                cleanNodes.update({node: nodes[node]})

    edges = []

    for way in ways:
        for n in range(len(way)-1):
            node1 = way[n]
            node2 = way[n+1]
            edges.append(Edge(node1,node2))

    nodes = cleanNodes

    return [nodes, edges]

if __name__ == "__main__":
    graph = getGraph('hervanta.osm')
    graphSize = getsizeof(graph[0])
    graphSize += sum(map(getsizeof, graph[0].values())) + sum(map(getsizeof, graph[0].keys()))
    graphSize += getsizeof(graph[1])
    print("Size: ",math.floor(graphSize/1000),"kB")
    print("Nodes:",len(graph[0]))
    print("Edges:",len(graph[1]))
    #plotGraph(graph[0],graph[1])

