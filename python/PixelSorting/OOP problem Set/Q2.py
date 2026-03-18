class Pet():
	def __init__(self, kind, num_legs):
		if not kind:
			raise ValueError
		self.kind = kind
		if num_legs < 0:
			raise ValueError
		self.num_legs = num_legs
  
	def get_kind(self):
		return self.kind
	def get_num_legs(self):
		return self.num_legs
	
	def set_kind(self,kind):
		if not kind:
			raise ValueError
		self.kind = kind
	def set_num_legs(self,num_legs):
		if num_legs < 0:
			raise ValueError
		self.num_legs = num_legs
		
	
	def run(self):
		print(f"{self.kind} is running")
	def stop(self):
		print(f"{self.kind} stopped")


dog = Pet("Dog", 4)
monkey = Pet("Monkey", 2)

#Cdog = Pet("", 4)
monkey = Pet("Monkey", -2)
