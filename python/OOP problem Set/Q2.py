class Pet():
    def __init__(self, kind, num_legs):
        if not kind:
            raise ValueError
        self.kind = kind
        if num_legs < 0:
            raise ValueError
        self.num_legs = num_legs
    def run(self):
        print(f"{self.kind} is running")
    def stop(self):
        print(f"{self.kind} stopped")


dog = Pet("Dog", 4)
monkey = Pet("Monkey", 2)

#dog = Pet("", 4)
#monkey = Pet("Monkey", -2)
