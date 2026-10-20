side_1 = int(input())
side_2 = int(input())
side_3 = int(input())

if side_1 == side_2 and side_1 == side_3:
    print("equilateral")
elif side_1 == side_2 or side_1 == side_3 or side_2 == side_3:
    print("isosceles")
else:
    print("scalene")
