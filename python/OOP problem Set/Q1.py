class Trigonometry():
    def square_area(self, length):
        return length * length
    
    def rectangle_area(self, length, height):
        return length * height
    
    def triangle_area(self, base, height):
        area = base * height 
        return area
    
trig = Trigonometry()


print(trig.square_area(int(input("Enter a square length"))))

print(trig.rectangle_area(int(input("Enter a rectangle length")), int(input("Enter a rectangle height"))))

print(trig.rectangle_area(int(input("Enter a triangle base")), int(input("Enter a traingle height"))))