class Cube():
	def __init__(self, side_length):
		if side_length <= 0:
			raise ValueError("Length must be a positive non zero value")
		self.side_length = side_length

	def display_volume(self):
		volume = self.side_length ** 3
		print(f"Volume of cube is {volume}")
	
	def display_surface(self):
		print(f"Surface area of one face of the cube is {self.side_length ** 2}")
		
	def display_total_surface(self): 
		print(f"Total surface area of cube is {6 * (self.side_length ** 2) }")
		
c = Cube(int(input("What is the side length of the cube: ")))

c.display_volume()
c.display_surface()
c.display_total_surface()
