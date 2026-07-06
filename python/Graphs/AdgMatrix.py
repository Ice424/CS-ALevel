import os
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.adj_matrix = [[0] * vertices for _ in range(vertices)]  # V x V matrix

    def add_edge(self, u, v, directional = False):
        """Adds an edge from vertex u to vertex v (undirected graph)."""
        self.adj_matrix[u][v] = 1
        if not directional:
            self.adj_matrix[v][u] = 1
            
    def get_edges(self, u):
        edges = []
        for v in range(len(self.adj_matrix[u])):
            if self.adj_matrix[u][v] == 1:
                edges.append(v)
        return edges

    def print_graph(self):
        """Prints the adjacency matrix."""
        print("Adjacency Matrix:")
        for row in self.adj_matrix:
            print(" ".join(str(val) for val in row))
    
    
    
    def gen_obsidian(self):
        os.makedirs("./Obsidian", exist_ok=True)
        for v in range(self.V):
            with open(f"./Obsidian/{v}.md", "w") as f:
                f.write(f"# {v}\n\n")
                for i in range(len(self.adj_matrix[v])):
                    if self.adj_matrix[v][i] == 1: 
                        f.write(f"[[{i}]]\n")
                        
    def save(self, file_path:str):
        with open(file_path, "w") as f:
            for row in self.adj_matrix:
                f.write(f"{"".join(str(val) for val in row)}\n")
                
    def load(self, file_path:str):
        
        with open(file_path, "r") as f:
            content = f.readlines()
            
        for i in range(len(content)):
            for j in range(len(content[i].strip())):
                self.adj_matrix[i][j] = int(content[i][j])
        
            


# Example usage:
if __name__ == "__main__":
    V = 10
    g = Graph(V)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(6, 7)
    g.add_edge(9,0, directional=True)
    g.print_graph()
    print(g.get_edges(1))
    g.gen_obsidian()
    g.load("file.txt")
    g.print_graph()
