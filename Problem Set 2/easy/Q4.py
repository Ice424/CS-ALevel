user_input = int(input())
total = 0

for i in range(user_input):
    if i >= 2:
        total = 10.5
    else:
        total += 7

print(total)