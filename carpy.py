# reading osm
import xml.etree.ElementTree

# plotting
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y, id):
        self.x = float(x)
        self.y = float(y)
        self.id = id
        self.neighbors = []

    def normalize(self, bounds):
        self.x = 1/(bounds['maxX']-bounds['minX'])*(self.x-bounds['minX'])*100
        self.y = 1/(bounds['maxY']-bounds['minY'])*(self.y-bounds['minY'])*100

    def addNeighbor(self, id):
        self.neighbors.append(id)

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

def plotGraph(graph):
    x = []
    y = []

    for key, node in graph.items():
        x.append(node.x)
        y.append(node.y)

    drawnNodes = []
    drawn = 0
    skipped = 0

    for key, node in graph.items():
        for edge in node.neighbors:
                node2 = graph[edge]
                if not node2 in drawnNodes:
                    plt.plot([node.x, node2.x],[node.y, node2.y])
                    drawn += 1
                else:
                    skipped += 1

        drawnNodes.append(node)

    print("Edges skipped:",skipped,"drawn",drawn)

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

def countEdges(graph):
    edges = 0
    for key, node in graph.items():
        edges += len(node.neighbors)
    return edges

def getGraph(fileName):
    nodes = {}

    osm = xml.etree.ElementTree.parse(fileName).getroot()
    for node in osm.findall('node'):
        newNode = Node(node.get('lon'),node.get('lat'),node.get('id'))
        nodes.update({newNode.id: newNode})

    ways = getWays(osm)

    cleanNodes = {}
    for way in ways:
        for node in way:
            if node in nodes.keys():
                cleanNodes.update({node: nodes[node]})
    nodes = cleanNodes

    for way in ways:
        for n in range(len(way)-1):
            node1 = way[n]
            node2 = way[n+1]
            nodes[node1].addNeighbor(node2)
            nodes[node2].addNeighbor(node1)

    return nodes

if __name__ == "__main__":
    graph = getGraph('lempaala.osm')
    print("Nodes:",len(graph))
    print("Edges:",countEdges(graph))

    plotGraph(graph)

