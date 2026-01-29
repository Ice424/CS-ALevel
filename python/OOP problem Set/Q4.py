class Box():
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
    def display_vol(self):
        print(f"Volume: {self.height * self.length * self.width}")
    
    def display(self):
        print(f"Width {self.width}")
        print(f"length {self.length}")
        print(f"height {self.height}")

theBox = Box(int(input("Enter the width: ")), int(input("Enter the length: ")), int(input("Enter the height: ")))
theBox.display_vol()
theBox.display()