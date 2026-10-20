class info():
	def __init__(self, user_text:str) -> None:
		if not user_text:
			raise ValueError("User text must not be empty")
		self.user_text = user_text
	
	def get_spaces(self) -> int:
		count = 0
		for char in self.user_text:
			if char == " ":
				count +=1
		return count
	
	def get_vowels(self) ->int:
		count = 0
		vowels="aiou"
		for char in self.user_text.lower():
			if char in vowels:
				count+=1
		
		return count
	
	def get_letters(self) -> int:
		count = 0
		for char in self.user_text:
			if char.isalpha and char != " ":
				count+=1
		return count
	
	def get_word_count(self) -> int:
		text = self.user_text.split(" ")
		count = len(text)
		return count
	
text = info(input("Enter some text:\n"))

print(f"num spaces: {text.get_spaces()}")
print(f"num vowels: {text.get_vowels()}")
print(f"num letters: {text.get_letters()}")
print(f"num words: {text.get_word_count()}")