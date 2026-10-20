class Queue:
    def __init__(self) -> None:
        self.items = []
    
    def __str__(self) -> str:
        return str(self.items)
    
    def is_empty(self) -> bool:
        return not self.items
    
    def enqueue(self, item) -> None:
        self.items.insert(0,item)
        
    def dequeue(self) -> object:
        if self.is_empty:
            return
        return self.items.pop()
    
    def size(self) -> int:
        return len(self.items)
    
    
            
    
q = Queue()

q.enqueue("test")

print(q.is_empty())
print(q.dequeue())