import math
a = float(input("a:\t"))
b = float(input("b:\t"))
c = float(input("c:\t"))

root1 = (-b + math.sqrt((b**2) - (4 * a * c))) / 2*a
root2 = (-b - math.sqrt((b**2) - (4 * a * c))) / 2*a

print(f"x = {root1} or {root2}")
