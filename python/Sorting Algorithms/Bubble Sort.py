items =  [456,24,56,12,26]

n = len(items)

comparisons = 0
exchanges = 0
passes = 0

swapped = True
while n > 0 and swapped == True:
    passes += 1
    swapped = False
    n = n - 1
    for index in range(0,n):
        comparisons +=1
        if items[index] > items[index+1]:
            exchanges += 1
            temp = items[index]
            items[index] = items[index+1]
            items[index+1]  =temp
            swapped = True
        #print(items)
#Output the result
print(items)

print("comparisons", comparisons)
print("exchanges", exchanges)
print("passes", passes)