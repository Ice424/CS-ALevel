import json
class stack:

    class current_vertex:
        data = None
        pointer = None

    stack_pointer = None

    def push(self,item):
        #Check stack overflow
        try:
            #Push the item
            new_current_vertex = stack.current_vertex()
            new_current_vertex.data = item
            new_current_vertex.pointer = self.stack_pointer
            self.stack_pointer = new_current_vertex
            return True
        except:
            return False

    def pop(self):
        #Check stack underflow
        if self.stack_pointer != None:
            #Pop the item
            popped = self.stack_pointer.data
            self.stack_pointer = self.stack_pointer.pointer
            return popped
        else:
            return None
    
#Main program starts here

def load(path) -> dict:
    with open(path, "r") as f:
        graph = json.loads(f.read())
    return graph
        
def dfs(graph):   
    visited = []
    s = stack()
    current_vertex = "A"
    while current_vertex != None:
        for vertex in reversed(graph[current_vertex]):
            if not vertex in visited:
                s.push(vertex)
        if not current_vertex in visited:
            visited.append(current_vertex)
        current_vertex = s.pop()
    print(visited)


graph = load("graph.json")
dfs(graph)