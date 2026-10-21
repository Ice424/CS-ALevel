
The complexity of algorithms can be measured in two ways

## Time Complexity

Time complexity is not measured in seconds due to differences in hardware speed

It is given in big O notation where N is the number of values inputted the formula should equal the amount of operations where N -> inf


```python
for i in range(n)
	n+=1
```

Would have time complexity O(n)


```python
for i in range(1000)
	n-=1

for i in range(n)
	n+=1
```

Would have time complexity O(n+1000) however as N->inf = O(n)

```python
for i in range(n):
	for j in range(n)
		n+=1

```
O(n^2)

## Space Complexity

The max amount of ram it uses

A recursive algorithm has infinite space complexity as n -> inf
