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
	def __init__(self):
		self.__rootNode = self.createBalancedTree()

	@property
	def rootNode(self):
		return self.__rootNode

	def createBalancedTree(self):
		node1 = Node(1)
		node2 = Node(2, node1)
		node4 = Node(4)
		node3 = Node(3, node2, node4)
		node6 = Node(6)
		node8 = Node(8)
		node7 = Node(7, node6, node8)
		node5 = Node(5, node3, node7)
		return node5

	
		

tree = Tree()

#print(tree.rootNode.value)
#print(tree.rootNode.right.value)
#print(tree.rootNode.left.value)
print(breadthFirstSearch(tree.rootNode))
input()
