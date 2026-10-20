# Written by Craig'n'Dave
# Circular queue using an array/list
class Queue:
    max = 8
    items = ["" for index in range(max)]

    front_pointer = -1
    back_pointer = -1

    def enqueue(self, item):
        # Check queue overflow
        if (self.back_pointer + 1) % self.max != self.front_pointer:
            self.back_pointer = (self.back_pointer + 1) % self.max
            # Enqueue the item
            self.items[self.back_pointer] = item
            # Set first item if queue was empty 
            if self.front_pointer == -1:
                self.front_pointer = 0
            return True
        else:
            return False

    def dequeue(self):
        # Check queue underflow
        if self.front_pointer != -1:
            # Dequeue the item
            item = self.items[self.front_pointer]
            # If the queue is not empty change the front pointer
            if self.front_pointer != self.back_pointer:
                self.front_pointer = (self.front_pointer + 1) % self.max
            else:
                # When the last item is dequeued reset the pointers
                self.front_pointer = -1
                self.back_pointer = -1
            return item
        else:
            return None

    def peek(self):
        # Check queue underflow
        if self.front_pointer != -1:
            # Peek the item
            return self.items[self.front_pointer]
        else:
            return None


# Main program starts here
items = ["Florida", "Georgia", "Delaware", "Alabama", "California"]
q = Queue()
# Add items to the queue
for index in range(0, len(items)):
    q.enqueue(items[index])
# Remove items from the queue
print(q.dequeue())
# Output the next item in the queue
print(q.peek())
