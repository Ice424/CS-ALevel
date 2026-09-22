Answer = 0
Column = 16
while not (Column < 1):
    bit = int(input("Enter bit value: "))
    Answer = Answer + (Column*bit)
    Column = Column/2

print("Decimal value is: ")
print(Answer)