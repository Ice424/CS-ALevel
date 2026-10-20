class Box():
	def __init__(self, width, length, height):
		if width <= 0:
			raise ValueError("Lengths cannot be negative or 0")
		self.width = width
  
		if length <= 0:
			raise ValueError("Lengths cannot be negative or 0")
		self.length = length
  
		if height <= 0:
			raise ValueError("Lengths cannot be negative or 0")
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