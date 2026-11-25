class Graph():
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def closestNode(self, currentNode, paths):
        startRow = ord(currentNode) - 65

        for edge in self.edges:
            if edge[0] == currentNode:
                endRow = ord(edge[1]) - 65
                if paths[endRow][1] == None or paths[endRow][1] > edge[2] + paths[startRow][1]:
                    paths[endRow][1] = edge[2] + paths[startRow][1]
                    paths[endRow][2] = currentNode

        nextNode = ''
        shortestDistance = 0
        for edge in self.edges:
            shortestDistance = shortestDistance + edge[2]
        for node in paths:
            if node[1] != None and node[1] < shortestDistance:
                shortestDistance = node[1]
                nextNode = node[0]

        return nextNode

nodes = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [['A', 'B', 24], ['A', 'C', 6], ['A', 'E', 13], ['B', 'E', 2], ['B', 'F', 1], ['C', 'D', 3], ['D', 'E', 2], ['E', 'F', 1]]
graph = Graph(nodes, edges)
paths = []
for node in nodes:
    paths.append([node, None, None])
startNode = 'A'
paths[ord(startNode)-65][1] = 0
print(graph.closestNode(startNode, paths))
input()