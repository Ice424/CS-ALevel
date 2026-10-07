# Written by Craig'n'Dave
# Binary tree using an array/list
class BinaryTree:

    depth = 5
    max = 2**(depth + 1) - 1
    btree = ["" for item in range(max)]
    root = 0
    
    def add(self, item):
        current_node = self.root
        # Find correct position
        while current_node < self.max and self.btree[current_node] != "":
            if item < self.btree[current_node]:
                current_node = (2 * current_node) + 1
            else:
                current_node = (2 * current_node) + 2
        # Check overflow
        if current_node < self.max:
            self.btree[current_node] = item
            return True
        else:
            return False

    def delete(self, item):
        # Using Hibbard's algorithm (leftmost node of right sub-tree is the successor)
        # Find the node to delete
        current_node = self.root
        while current_node < self.max and self.btree[current_node] != item:
            if item < self.btree[current_node]:
                current_node = (2 * current_node) + 1
            else:
                current_node = (2 * current_node) + 2
        if current_node < self.max and self.btree[current_node] == item:
            # Handle 3 cases depending on the number of child nodes
            left_node = (2 * current_node) + 1
            right_node = (2 * current_node) + 2
            if left_node < self.max and self.btree[left_node] == "" and right_node < self.max and self.btree[right_node] == "":
                # Node has no children
                self.btree[current_node] = ""
            elif left_node < self.max and self.btree[left_node] != "" and right_node < self.max and self.btree[right_node] != "":
                # Node has two children
                # Find the smallest value in the right sub-tree (successor node)
                smallest = right_node
                while (2 * smallest) + 1 < self.max and self.btree[(2 * smallest) + 1] != "":
                    smallest = (2 * smallest) + 1
                self.btree[current_node] = self.btree[smallest]
                self.btree[smallest] = ""
            elif left_node < self.max and self.btree[left_node] != "":
                # Node has one left child
                self.btree[current_node] = self.btree[left_node]
                self.btree[left_node] = ""
            elif right_node < self.max and self.btree[right_node] != "":
                # Node has one right child
                self.btree[current_node] = self.btree[right_node]
                self.btree[right_node] = ""        
            return True
        else:
            return False
        
    def preorder(self, current_node):
        # Visit each node: NLR
        if current_node < self.max and self.btree[current_node] != "":
            print(self.btree[current_node])
            self.preorder((2 * current_node) + 1)
            self.preorder((2 * current_node) + 2)

    def inorder(self, current_node):
        # Visit each node: LNR
        if current_node < self.max and self.btree[current_node] != "":
            self.inorder((2 * current_node) + 1)
            print(self.btree[current_node])
            self.inorder((2 * current_node) + 2)

    def postorder(self, current_node):
        # Visit each node: LRN
        if current_node < self.max and self.btree[current_node] != "":
            self.postorder((2 * current_node) + 1)
            self.postorder((2 * current_node) + 2)
            print(self.btree[current_node])

    def bft(self):
        # Visit each node: BFT
        for current_node in range(self.max):
            if self.btree[current_node] != "":
                print(self.btree[current_node])


# Main program roots here
items = [56, 26, 200, 18, 28, 190, 213, 12, 24, 27]
binary_tree = BinaryTree()
for index in range(0, len(items)):
    binary_tree.add(items[index])
# Traverse the binary tree
print("Breadth first traversal:")
binary_tree.bft()








