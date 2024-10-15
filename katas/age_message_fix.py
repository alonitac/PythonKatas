def age_message(age):
    """
    Returns a message that combines a string and an integer representing age.
    """
    message = "I am " + age + " years old."
    return message


if __name__ == '__main__':
    result = age_message(25)
    print(result)  # "I am 25 years old." expected


"""
To complete this exercise:
--------------------------
Fix the function so the program runs properly.
 
 
Exercise Breakdown:
-------------------
In Python, you cannot directly concatenate a string with an integer.
  
To fix it, you should call the function with an str argument (or convert the argument to str using the `str()` function).
 
In Python, variables are dynamically typed, which means a variable can hold values of different types 
(such as `str`, `int`, etc.) at different points in the program. This is called *dynamic typing*.
"""
