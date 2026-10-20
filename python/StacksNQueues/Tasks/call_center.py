import random
import time
import names
from linear_queue import Queue

calls = Queue(20)

class Call():
    def __init__(self) -> None:
        self.name: str = str(names.get_full_name())
        self.number = "07" + str(random.randint(100000000, 999999999))
        self.time = random.randint(1,20)

class Assistant():
    def __init__(self) -> None:
        self.name: str = str(names.get_full_name())
        self.current_call: None|Call = None
        self.time_remaining:int = 0

assistants = [Assistant(), Assistant()]

while True:
    if random.randint(0,3) == 0:
        calls.enQueue(Call())
    
    
    print("\n")
    for assistant in assistants:
        if assistant.current_call == None and not calls.isEmpty():
           assistant.current_call = calls.queueFront()
           assistant.time_remaining = assistant.current_call.time # pyright: ignore[reportOptionalMemberAccess]
           calls.deQueue()
           print(f"{assistant.name} started a call with {assistant.current_call.name} for {assistant.time_remaining} more seconds")
           
        elif assistant.current_call:
            assistant.time_remaining -= 1
            print(f"{assistant.name} is on call with {assistant.current_call.name} for {assistant.time_remaining} more seconds")
            if assistant.time_remaining == 0:
                assistant.current_call = None

    if calls.size >= 5 and len(assistants) == 2:
        assistants.append(Assistant())
        
    elif calls.size < 5 and len(assistants) != 2:
        if assistants[-1].current_call == None:
            assistants.pop(-1)
    
    print(f"There are {calls.size} people in the queue")
    time.sleep(1)
    