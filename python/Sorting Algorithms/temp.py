sum = 0
key = "NEP"

for i in range(len(key)):
    sum = sum + ord(key[i]) * ord(key[i])

print(sum%523)