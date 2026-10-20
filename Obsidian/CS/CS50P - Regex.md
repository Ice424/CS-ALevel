### Search
```python
re.search()
```
Finds the first match anywhere in the string

Example:
```python
re.search("cat", "the cat naps")
```

checking if a pattern exists at all.

### Match
```python
re.match()
```
Matches only at the start of the string

Example:
```python
re.match("cat", "catnap")
```

Fails if the pattern doesn’t start at index 0.

### Full match
```python
re.fullmatch()
```
Matches the entire string

Example:
```python
re.fullmatch(r"\d+", "123")
```

Use when: validating input.

### Find All
```python
re.findall()
```
Returns all matches as a list

Example:
```python
re.findall(r"\d+", "a1 b22")
```
Result: ['1', '22']

Use when: extracting data.

### Find iterable
```python
re.finditer()
```
Returns match objects (with positions)

Example:
```python
for m in re.finditer(r"\d+", "a1 b22"):
    m.group()
```

Use when: you need indexes or metadata.

### Substitute
```python
re.sub()
```
Replaces matches

Example:
```python
re.sub(r"\d+", "#", "Room 42")
```
Result: Room #

Use when: cleaning or reformatting text.

### Split
```python
re.split()
```
Splits using a regex pattern

Example:
```python
re.split(r"[,\s]+", "a, b  c")
```
Result: ['a', 'b', 'c']


# Uses of RegEx
- Searching for patterns in text.
- Extracting parts of strings.
- Replacing or cleaning up text .


(?:) - non capturing parenthesises
