import shutil
from pathlib import Path
import os
import re

class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        
        self.distance = 9999
        self.color = 'black'
    
    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()

class Graph:
    vertices = {}
    
    def add_vertex(self, vertex: Vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return vertex
        else:
            return self.vertices[vertex.name]
    
    def add_edge(self, u:str, v:str):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.add_neighbor(v)
                if key == v:
                    value.add_neighbor(u)
            return True
        else:
            return False
            
    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbors) + "  " + str(self.vertices[key].distance))
        
    def bfs(self, vert):
        q = list()
        vert.distance = 0
        vert.color = 'red'
        for v in vert.neighbors:
            self.vertices[v].distance = vert.distance + 1
            q.append(v)
        
        while len(q) > 0:
            u = q.pop(0)
            node_u = self.vertices[u]
            node_u.color = 'red'
            
            for v in node_u.neighbors:
                node_v = self.vertices[v]
                if node_v.color == 'black':
                    q.append(v)
                    if node_v.distance > node_u.distance + 1:
                        node_v.distance = node_u.distance + 1
      
    def export(self, export_path):
        shutil.rmtree(export_path)
        os.mkdir(export_path)
        for vertex in g.vertices.values():
            with open(f"./{export_path}/{vertex.name}.md", "w") as f:
                for connection in vertex.neighbors:
                    f.write(f"[[{connection}]]\n")
    
    def import_graph(self, import_path):
        for (root,dirs,files) in os.walk(import_path):
            for file in files:
                path = Path(os.path.abspath( os.path.join(root, file)))
                name = path.stem
                if not str(path).endswith(".md"):
                    continue
                with open(path, "r") as f:
                    connections = re.findall("\\[\\[(\\w+)\\]\\]", f.read())
                v = Vertex(name)
                v = self.add_vertex(v)
                for connection in connections:
                    u = Vertex(connection)
                    u = self.add_vertex(u)
                    self.add_edge(v.name, u.name)

                    
g = Graph()

 
g.import_graph("Obsidian")
v = g.add_vertex(Vertex("A"))
g.bfs(v)
g.print_graph()
