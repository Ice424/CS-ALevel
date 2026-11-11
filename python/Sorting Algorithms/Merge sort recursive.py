def mergeSort(items):
    print("Splitting ",items)
    if len(items)>1:
        mid=len(items)//2
        lefthalf=items[:mid]
        righthalf=items[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        print("Merging ",items)
        while i < len(lefthalf) and j <len(righthalf):
            if lefthalf[i]<righthalf[j]:
                items[k]=lefthalf[i]
                i=i+1
            else:
                items[k]=righthalf[j]
                j=j+1
            k=k+1
            
        while i <len(lefthalf):
            items[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            items[k]=righthalf[j]
            j=j+1
            k=k+1

items = [9,8,7,6,5,4,3,2,1,0]
mergeSort(items)
print(items)
