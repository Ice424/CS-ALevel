class Event:
    def __init__(self, name: str, start_time: int):
        self.name = name
        self.start_time = start_time

    def __str__(self):
        return f"{self.start_time:04d} - {self.name}"


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, event: Event):
        position = 0

        while (
            position < len(self.queue)
            and self.queue[position].start_time <= event.start_time
        ):
            position += 1

        self.queue.insert(position, event)

    def dequeue(self):
        if self.is_empty():
            raise IndexError

        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None

        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)




pq = PriorityQueue()

for i in range(7):
    name = input(f"Enter event {i + 1} name: ")
    start_time = int(input("Enter start time (HHMM): "))
    pq.enqueue(Event(name, start_time))



print("\nNext event:")
print(pq.dequeue())