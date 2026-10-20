def dfs(graph, current_vertex):
    visited.append(current_vertex)
    for vertex in graph[current_vertex]:
        if not vertex in visited:
            dfs(graph, vertex)
    
#Main program starts here
graph = {"A":["B", "C"], "B": ["E", "F"], "C":["D", "G"], "D": [], "E": [], "F": [], "G": []}
visited = []
dfs(graph,"A")
print(visited)
