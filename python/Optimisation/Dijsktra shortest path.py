def dijkstra(graph,start,goal):
    #Initialise
    infinity = float("inf")
    distance = {}
    previous_vertex = {}
    shortest_path = []

    #Set the shortest distance from the start for all vertices to infinity
    for vertex in graph:
        distance[vertex] = infinity
    #Set the shortest distance from the start for the start vertex to 0
    distance[start] = 0
   
    #Loop until all the vertices have been visited
    while graph:
        #Find the vertex with the shortest distance from the start
        shortest = None
        for vertex in graph:
            if shortest == None:
                shortest = vertex
            elif distance[vertex] < distance[shortest]:
                shortest = vertex

        #Calculate shortest distance for each edge
        for neighbour, cost in graph[shortest].items():
            #Update the shortest distance for the vertex if the new value is lower
            if neighbour in graph and cost + distance[shortest] < distance[neighbour]:
                distance[neighbour] = cost + distance[shortest]
                previous_vertex[neighbour] = shortest
                
        #The vertex has now been visited, remove it from the vertices to consider
        graph.pop(shortest)

    #Generate the shortest path
    #Start from the goal, adding vertices to the front of the list
    vertex = goal
    while vertex != start:
        shortest_path.insert(0,vertex)
        vertex = previous_vertex[vertex]
    #Add the start vertex
    shortest_path.insert(0,start)
    
    #Return the shortest shortest_path
    return shortest_path

#Main program starts here
graph = {"A":{"B":2, "C": 4},"B":{"A":2, "C":1, "D":4, "E": 2},"C":{"A":4, "B":1, "E":1},"D":{"B":4,"E":3,"F":2},"E":{"B":2,"D":3, "F":2},"F":{"D":2,"E":5}}
print(dijkstra(graph, "A", "F"))
