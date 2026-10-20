# Written by Craig'n'Dave
# Binary tree using objects
class Queue:
    
    class Node:
        data = None
        pointer = None

    front_pointer = None
    back_pointer = None

    def enqueue(self, item):
        # Check queue overflow
        try:
            # Push the item
            new_node = Queue.Node()
            new_node.data = item
            # Empty queue
            if self.back_pointer == None:
                self.front_pointer = new_node
            else:
                self.back_pointer.pointer = new_node
            self.back_pointer = new_node
            return True
        except:
            return False

    def dequeue(self):
        # Check queue underflow
        if self.front_pointer != None:
            # Dequeue the item
            popped = self.front_pointer.data
            self.front_pointer = self.front_pointer.pointer
            # When the last item is dequeued reset the pointers
            if self.front_pointer == None:
                self.back_pointer = None
            return popped
        else:
            return None

    def peek(self):
        # Check queue underflow
        if self.front_pointer != None:
            # Peek the item
            return self.front_pointer.data
        else:
            return None


class Binary_tree:
    class Node:
        data = None
        left_pointer = None
        right_pointer = None

    root = None

    def add(self, item):
        # Check memory overflow
        try:
            new_node = Binary_tree.Node()
            new_node.data = item
            current_node = self.root
            new_node.left_pointer = None
            new_node.right_pointer = None
            # Tree is empty
            if current_node == None:
                self.root = new_node
            else:
                # Find correct position in the tree
                while current_node != None:
                    previous = current_node
                    if item < current_node.data:
                        current_node = current_node.left_pointer
                    else:
                        current_node = current_node.right_pointer
                if item < previous.data:
                    previous.left_pointer = new_node
                else:
                    previous.right_pointer = new_node
                return True
        except:
            return False

    def delete(self, item):
        # Using Hibbard's algorithm (leftmost node of right sub-tree is the successor)
        # Find the node to delete
        current_node = self.root
        while current_node != None and current_node.data != item:
            previous = current_node
            if item < current_node.data:
                current_node = current_node.left_pointer
            else:
                current_node = current_node.right_pointer

        # Handle 3 cases depending on the number of child nodes
        if current_node != None:
            if current_node.left_pointer == None and current_node.right_pointer == None:
                # Node has no children
                if previous.data > current_node.data:
                    previous.left_pointer = None
                else:
                    previous.right_pointer = None
            elif current_node.right_pointer == None:
                # Node has one left child
                if previous.data > current_node.data:
                    previous.left_pointer = current_node.left_pointer
                else:
                    previous.right_pointer = current_node.left_pointer
            elif current_node.left_pointer == None:
                # Node has one right child
                if previous.data < current_node.data:
                    previous.left_pointer = current_node.right_pointer
                else:
                    previous.right_pointer = current_node.right_pointer
            else:
                # Node has two children
                right_node = current_node.right_pointer
                if right_node.left_pointer != None:
                    # Find the smallest value in the right sub-tree (successor node)
                    smallest = right_node
                    while smallest.left_pointer != None:
                        previous = smallest
                        smallest = smallest.left_pointer
                    # Change the deleted node value to the smallest value
                    current_node.data = smallest.data
                    # Remove the successor node
                    previous.left_pointer = None
                else:
                    # Handle special case of no left sub-tree from right node
                    current_node.data = right_node.data
                    current_node.right_pointer = None

    def preorder(self, current_node):
        if current_node != None:
            # Visit each node: NLR
            print(current_node.data)
            if current_node.left_pointer != None:
                self.preorder(current_node.left_pointer)
            if current_node.right_pointer != None:
                self.preorder(current_node.right_pointer)

    def inorder(self, current_node):
        if current_node != None:
            # Visit each node: LNR
            if current_node.left_pointer != None:
                self.inorder(current_node.left_pointer)
            print(current_node.data)
            if current_node.right_pointer != None:
                self.inorder(current_node.right_pointer)

    def postorder(self, current_node):
        if current_node != None:
            # Visit each node: LRN
            if current_node.left_pointer != None:
                self.postorder(current_node.left_pointer)
            if current_node.right_pointer != None:
                self.postorder(current_node.right_pointer)
            print(current_node.data)

    def bft(self, current_node):
        q = Queue()
        # Visit each node: BFT
        while current_node != None:
            print(current_node.data)
            if current_node.left_pointer != None:
                q.enqueue(current_node.left_pointer)
            if current_node.right_pointer != None:
                q.enqueue(current_node.right_pointer)
            current_node = q.dequeue()


# Main program starts here
items = ["E", "B", "G", "A", "C", "F", "H"]
# Create binary tree
binary_tree = Binary_tree()
for index in range(0, len(items)):
    binary_tree.add(items[index])
# Traverse the binary tree
print("Breadth first traversal:")
binary_tree.bft(binary_tree.root)
print("Pre-order traversal:")
binary_tree.preorder(binary_tree.root)
print("In-order traversal:")
binary_tree.inorder(binary_tree.root)
print("Post-order traversal:")
binary_tree.postorder(binary_tree.root)
