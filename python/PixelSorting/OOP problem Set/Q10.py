def display_menu():
	menu_items = ["Enter encryption/decryption key", "Encrypt a message", "Decrypt a message", "Exit"]
	
	for i in range(len(menu_items)):
		print(f"{i+1}: {menu_items[i]}")


class EncryptDecrypt:
	
	def __init__(self) -> None:
		self.key:int

	def set_key(self) -> None:
		key = int(input("What should the Key be: "))
		if key < 1 or key > 26:
			raise ValueError("Key must be between 1-26 inclusive")
		self.key = key
	
	def get_key(self) -> int:
		try:
			return self.key
		except AttributeError:
			raise ValueError("Key not set")
	
	def encrypt(self) -> str:
		plaintext = input("Text to be encrypted: ")
		ciphertext = ""
		for char in plaintext:
			cipher_num = ord(char) + self.get_key()
			if cipher_num > 126:
				cipher_num -= 95
			ciphertext += chr(cipher_num)
		return ciphertext
	
	def decrypt(self) -> str:
		ciphertext = input("Text to be decrypted: ")
		plaintext = ""
		for char in ciphertext:
			cipher_num = ord(char) - self.get_key()
			if cipher_num < 32:
				cipher_num += 95
			plaintext += chr(cipher_num)
		return plaintext

ed = EncryptDecrypt()

user_input = 0

while user_input != 4:
	display_menu()
	user_input = int(input("Choose an option: "))
	
	match user_input:
		case 1:
			ed.set_key()
		case 2:
			input(ed.encrypt())
		case 3:
			input(ed.decrypt())
