class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    
def depthFirstSearch(rootnode) -> list:
    ls = []
    if rootnode is None:
        return ls
    ls += depthFirstSearch(rootnode.left)
    ls += depthFirstSearch(rootnode.right)
    ls.append(rootnode.value)
    return ls

def breadthFirstSearch(rootnode) -> list:
    q = []
    visited = []
    q.append(rootnode)
    
  
    while q:
        curr = q.pop(0)
        visited.append(curr.value)
        if curr.left:
            q.append(curr.left)
        if curr.right:
            q.append(curr.right)
    
    return visited

    

class Tree:
    def __init__(self, nodes:list):
        self.__rootNode = self.createBalancedTree(nodes, 0, len(nodes)-1)

    @property
    def rootNode(self):
        return self.__rootNode

    def createBalancedTree(self, nodes, start, end):
        if start > end:
            return None


        mid = (start + end) // 2
        root = Node(nodes[mid])

        root.left = self.createBalancedTree(nodes, start, mid - 1)
        root.right = self.createBalancedTree(nodes, mid + 1, end)

        return root
    
    def binarySearch(self, target):
        current_node = self.__rootNode
        if not current_node:
            return Node(-1)
        
        while current_node.value != target:
            print(current_node.value)
            
            if current_node.value < target and current_node.right:
                current_node = current_node.right
                
                
            elif current_node.value > target and current_node.left:
                current_node = current_node.left
                
                
            else:
                print("Value not in tree")
                return Node(-1)
            
        return current_node
    
    def getParent(self, target):
            current_node = self.__rootNode
            if not current_node:
                return (None, "")
            while current_node.value != target:
                
                if current_node.value < target and current_node.right:
                    if current_node.right.value == target:
                        return (current_node, "right")
                    current_node = current_node.right
                    
                    
                elif current_node.value > target and current_node.left:
                    if current_node.left.value == target:
                        return (current_node, "left")
                    current_node = current_node.left
                    
                    
    def deleteNode(self, target):
        node: Node = self.binarySearch(target)
        parent, side = self.getParent(target)
        
        
        if node.left and node.right:
            setattr(parent, side, Node(node.left.value, None, node.right))
        elif node.left:
            setattr(parent, side, node.left)
        elif node.right:
            setattr(parent, side, node.right)
        else:
            setattr(parent, side, None)
    
    def addNode(self, target):
        current_node = self.__rootNode

        if not current_node:
            self.__rootNode = Node(target)
            return

        while True:
            if target < current_node.value:
                if current_node.left:
                    current_node = current_node.left
                else:
                    current_node.left = Node(target)
                    return

            elif target > current_node.value:
                if current_node.right:
                    current_node = current_node.right
                else:
                    current_node.right = Node(target)
                    return

            else:
                return
        
            
        
        
                
                
        
        
        
        


    
        

tree = Tree([1,2,3,4,5,6,7,8])

#print(tree.rootNode.value)
#print(tree.rootNode.right.value)
#print(tree.rootNode.left.value)
print(breadthFirstSearch(tree.rootNode))
print(depthFirstSearch(tree.rootNode))

print(tree.binarySearch(1).value)
print("\n")
print(tree.binarySearch(2).value)
print("\n")
print(tree.binarySearch(4).value)
print("\n")
print(tree.binarySearch(5).value)
print("\n")
print(tree.binarySearch(9).value)
print("\n")

print("\n")
tree.deleteNode(2)
print("\n")
print(tree.binarySearch(1).value)
print("\n")
print(tree.binarySearch(2).value)
print("\n")
print(tree.binarySearch(3).value)
print("\n")

tree.addNode(9)
tree.addNode(10)
tree.addNode(14)

print(tree.binarySearch(9).value)
print("\n")
print(tree.binarySearch(10).value)
print("\n")
print(tree.binarySearch(11).value)
print("\n")
print(tree.binarySearch(12).value)
print("\n")
print(tree.binarySearch(13).value)
print("\n")
print(tree.binarySearch(14).value)
print("\n")
print(tree.binarySearch(15).value)
print("\n")
input()
