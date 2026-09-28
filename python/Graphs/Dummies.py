import json

def write_file(graph, path) -> None:
    with open(path, "w") as f:
        f.write(json.dumps(graph))

def read_file(path) -> dict:
    with open(path, "r") as f:
        graph = json.loads(f.read())
    
    return graph

def bfs(graph,start):
    queue = [start]
    queued = []
    path = []
    while queue:
        print("Queue is: %s" % queue)
        vertex = queue.pop(0)
        print("Processing %s" % vertex)
        for candidate in graph[vertex]:
            if candidate not in queued:
                queued.append(candidate)
                queue.append(candidate)
                path.append(vertex+">"+candidate)
                print("Adding %s to the queue" % candidate)
    return path

graph = read_file("save_graph.json")
steps = bfs(graph,"A")
print("\nBFS:", steps)
    

