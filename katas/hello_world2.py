def create_greeting():
    """
    Returns a complete greeting message by concatenating strings.
    """
    greeting = "Hello"
    name = 'world'


if __name__ == '__main__':
    result = create_greeting()
    print(result)  # "Hello, world!" expected


"""
To complete this exercise:
--------------------------
Complete the 'create_greeting' function by concatenating the `greeting` and `name` variables 
with a comma and space in between, and add an exclamation mark at the end.


Exercise Breakdown:
-------------------
In Python, strings are sequences of characters, wrapper by "..." or '...' (there is not difference).
In order to concatenate two strings, use the `+` operator.
"""
