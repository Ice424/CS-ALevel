class binary_tree:

    class node:
        data = None
        left_pointer = None
        right_pointer = None

    start = None

    def add(self,item):
        #Check memory overflow
        try:
            new_node = binary_tree.node()
            new_node.data = item   
            current_node = self.start
            new_node.left_pointer = None
            new_node.right_pointer = None
            #Tree is empty
            if current_node == None:
                self.start = new_node
            else:
                #Find correct position in the tree
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

    def delete(self,item):
        #Using Hibbard's algorithm (leftmost node of right sub-tree is the successor)   
        #Find the node to delete
        current_node = self.start
        while current_node != None and current_node.data != item:
            previous = current_node
            if item < current_node.data:
                current_node = current_node.left_pointer
            else:
                current_node = current_node.right_pointer

        #Handle 3 cases depending on the number of child nodes
        if current_node != None:
            if current_node.left_pointer == None and current_node.right_pointer == None:
                #Node has no children
                if previous.data > current_node.data:
                    previous.left_pointer = None
                else:
                    previous.right_pointer = None
            elif current_node.right_pointer == None:
                #Node has one left child
                if previous.data > current_node.data:
                    previous.left_pointer = current_node.left_pointer
                else:
                    previous.right_pointer = current_node.left_pointer
            elif current_node.left_pointer == None:
                #Node has one right child
                if previous.data < current_node.data:
                    previous.left_pointer = current_node.right_pointer
                else:
                    previous.right_pointer = current_node.right_pointer
            else:
                #Node has two children
                right_node = current_node.right_pointer
                if right_node.left_pointer != None:
                    #Find the smallest value in the right sub-tree (successor node)
                    smallest = right_node
                    while smallest.left_pointer != None:
                        previous = smallest
                        smallest = smallest.left_pointer
                    #Change the deleted node value to the smallest value
                    current_node.data = smallest.data
                    #Remove the successor node
                    previous.left_pointer = None
                else:
                    #Handle special case of no left sub-tree from right node
                    current_node.data = right_node.data
                    current_node.right_pointer = None

           
    def preorder(self,current_node):
        if current_node != None:
            #Visit each node: NLR
            print(current_node.data)
            if current_node.left_pointer != None:
                self.preorder(current_node.left_pointer)
            if current_node.right_pointer != None:
                self.preorder(current_node.right_pointer)

    def inorder(self,current_node):
            if current_node != None:
                #Visit each node: LNR
                if current_node.left_pointer != None:
                    self.inorder(current_node.left_pointer)
                print(current_node.data)
                if current_node.right_pointer != None:
                    self.inorder(current_node.right_pointer)

    def postorder(self,current_node):
            if current_node != None:
                #Visit each node: LRN
                if current_node.left_pointer != None:
                    self.postorder(current_node.left_pointer)
                if current_node.right_pointer != None:
                    self.postorder(current_node.right_pointer)
                print(current_node.data)

#Main program starts here            
items = ["E","B","G","A","C","F","H"]
bt = binary_tree()
for index in range(0,len(items)):
    bt.add(items[index])
bt.inorder(bt.start)
bt.delete("F")
