x = 10

def linearSearch(searchList, searchVal):
    count = 0
    for i in range(len(searchList)):
        count += 1
        if searchList[i] == searchVal:
            return count
    return "Value not found"



def BinarySearch(searchList, searchVal):
    count = 0
    start = 0
    end = len(searchList) - 1
    while start <= end:
       
        mid = ((start + end) // 2)
        if searchList[mid] == searchVal:
            return count
        elif searchList[mid] < searchVal:
            count += 1
            start = mid+1
        elif searchList[mid] > searchVal:
            count += 1
            end = mid-1
    return "Value not found"

def recursiveBinarySearch(searchList,searchVal, low=0, high=None):
    if high is None:
        high = len(searchList)-1

    if high >= low:

        mid = low + (high - low) // 2

        if searchList[mid] == searchVal:
            return mid
        elif searchList[mid] > searchVal:
            return recursiveBinarySearch(searchList, searchVal ,low, mid-1)
        else:
            return recursiveBinarySearch(searchList, searchVal, mid + 1, high)
    else:
        return "Value Not Found"

def getVal() -> int | None:
    try:
        val = int(input("Enter a value: "))
        return val
    except Exception:
        print("Not accepted")
        return None

def generateList(val = None):
    while val is None:
        val = getVal()
    userlist = [i for i in range(val)]
    return userlist

def test(n, tests):
    searchList = generateList(n) 
    resultsBinary = 0
    resultsLinear = 0
    for i in range(tests):
        resultsBinary += BinarySearch(searchList, i)
        resultsLinear += linearSearch(searchList, i)
    averageBinary = (resultsBinary / tests) * 100
    averageLinear = (resultsLinear / tests) * 100
    
    print(f"Average binary search length: {averageBinary}")
    print(f"Average linear search length: {averageLinear}")
        

test(10,10)
input()
