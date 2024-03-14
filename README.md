# Python CLI Learner - v0.3
Simple, python based CLI learner, for learning by repetition.

---
## Main Functions

### Set from file
reads a file to create a set. An example file is provided [here](./example.txt)
```python
example = set_from_file(
    file_name="example.txt",
    set_name="default",         # default value, optional
    card_delimiter="\n",        # default value, optional
    definition_delimiter=" - ", # default value, optional
    hint_delimiter=". "         # default value, optional
)
```
## Learn
every term is asked at least 6 times, 3 times as multiple choice and 3 times as write answer. finishes when every term has been answered successfully 6 times in a row.
when answered incorrectly, the user has to try again later, and one streak is removed.

optional parameter: round size - how many terms are asked before option to quit

```python
example.learn(round_length=7)    # default round size
```

### Test
a small test with random terms. has multiple choice, write answer, connect and true/false.

```python
# test
example.test()
```

### Flashcards
simple look through of terms. can flip each term to show term/definition

```python
# flashcards
example.flashcards()
```

### Full Example
```python
if __name__ == "__main__":
    example = set_from_file("example.txt")

    # learn
    example.learn(round_length=7)

    # test
    # example.test()

    # flashcards
    # example.flashcards()
```

### Building sets in code
You can also create sets in code, if you do not want to worry about the file structure

#### usage
```python
# create new set
example = LearnSet(name="example")

# add terms
example.add(
    LearnObject(
        term="term1", 
        definition="Definition - hint1. hint2.", 
        year="year1",           # optional
        hint_delimiter=". "     # default value, optional
    )
)

# optional: save set, to load later
save_set_to_file(
    file_name="example_set",
    set=example
    # optionally add custom delimiters
)
```

### Set Union
Sets can also be unified with + operator
```python
union_set = example_set + another_set
```
This is useful if you have sets in different files and want to learn them all together at some point.
```python
massive_set = 
    set_from_file("one") + 
    set_from_file("two") + 
    set_from_file("three") # + ...
```

### Excercises
```python
multiple_choice(nr_options: int, correct: LearnObject = None)
write_answer(correct: LearnObject = None)
year(correct: LearnObject = None, ask: bool = True)
connect(nr_options: int = 8)
true_false()
```

### Patch notes:
```python
"""
0.1:
    1. Added 4 exercises (write, multiple choice, connect and true/false) and 2 joint exercises (learn and test).
    2. Added LearnObject and LearnSet classes
    3. Added Set from a file functionality with custom hint, term and definition splitters
    4. Added definition censoring
    5. Added addition of two sets
    6. Added set save to file functionality
0.2:
    1. Answer check is now lowercased (answer can be RaNDOmLy CapITAlizED, and should still give correct as long as letters are correct)
    2. Answers will only give the overwrite option when a typo is detected, typo threshold can be modified with set.min_ratio variable
    3. Fixed addition of two sets. Can create a union of learning sets by adding them together (+)
    4. Check connect now checks for missing answers and gives feedback
    5. removed 'Sets/' from set_from_file function
    6. added hint_delimiter variable for more scalability
    7. checks are now under each exercise, rather than having to call them out on their own. This means exercises can now be called one-by-one using the set.exercise_name() method
    8. added test configuration as a list. Enables the ability to create your own tests.
    9. added docstrings for classes and functions
    10. fixed equation with LearnSet objects. equation is now lower cased
0.21:
    1. Added set info after loading the set
    2. get_result now only shows learned terms, and the total, also shows after each round
    3. added round number to the message after the round
    4. fixed python magic: set_from_file now creates an EMPTY set beforehand
0.3:
    1. Added flipcards function
    2. Added {optional} year field to LearnObjects. Years are read like a definition - split the same. To mark a year in file use format: term {splitter} year {splitter} definition
"""
```