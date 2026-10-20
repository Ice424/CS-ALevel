class Queue():
    def __init__(self, size) -> None:
        self.queue = [None for i in range(size)]
        self.size = size
        self.front = -1
        self.back = -1
    
    def enqueue(self, item):
        if ((self.back + 1) % self.size == self.front):
            raise 
        elif (self.front == -1):
            self.front = 0
            self.back = 0
            self.queue[self.back] = item
        else:
            self.back = ( self.back + 1) % self.size
            self.queue[ self.back] = item

    def dequeue(self):
        if self.front == -1:
            return
        
        elif (self.front == self.back):
            temp = self.queue[self.front]
            self.front = -1
            self.back = -1
            return temp
        else:
            temp = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return temp
    
    def get_queue(self) -> list:
        if(self.front == -1):
            return []

        elif (self.back >= self.front):
            return [self.queue[i] for i in range(self.front, self.back + 1)]
        else:
            front_list = [self.queue[i] for i in range(self.front, self.size)]
            back_list = [self.queue[i] for i in range(0, self.back + 1)]
            return front_list + back_list
    
    def peek(self):
        if self.front == -1:
            return
        return self.queue[self.front]
        
        
q = Queue(6)
names = ["Ali", "Ben" , "Charlie", "Enid", "Fred"]
for name in names:
    q.enqueue(name)

q.get_queue()

q.dequeue()
q.dequeue()
q.dequeue()


q.enqueue("Greg")
q.enqueue("Freya")

print(q.queue)
print(q.get_queue())
print(q.peek())


