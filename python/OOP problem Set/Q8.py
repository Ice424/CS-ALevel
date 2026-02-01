import math
def display_menu():
	menu_items = ["Enter radius", "Display radius", "Display diameter", "Display area", "Display perimeter", "Exit"]
	
	for i in range(len(menu_items)):
		print(f"{i+1}: {menu_items[i]}")

class Circle():
	def __init__(self) -> None:
		self.radius: int|float 

	def set_radius(self) -> None:
		radius = int(input("What should the radius be: "))
		if radius <= 0:
			raise ValueError("Radius must be a positive non zero value")
		self.radius = radius
	
	def get_radius(self) -> int|float:
		try:
			return self.radius
		except AttributeError:
			raise ValueError("Radius not set")
		

	def get_diameter(self) -> int|float: 
		return (self.get_radius() * 2)
	
	def get_area(self) -> float:
		area = math.pi * (self.get_radius() **2)
		return area
	
	def get_perimeter(self) -> float:
		perimeter = self.get_diameter() * math.pi
		
		return perimeter

c = Circle()

user_input = 0

while user_input != 6:
	display_menu()
	user_input = int(input("Choose an option: "))
	
	match user_input:
		case 1:
			c.set_radius()
		case 2:
			input(c.get_radius())
		case 3:
			input(c.get_diameter())
		case 4:
			input(c.get_area())
		case 5:
			input(c.get_perimeter())