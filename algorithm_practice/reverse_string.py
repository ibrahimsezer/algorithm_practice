
"""
Given a string, write an algorithm to reverse the order of words in the string.
"""


def reverse_string(val: str):
    new_val = val.split(" ")
    new_val.reverse()
    reversed_text = " ".join(new_val)
    return reversed_text

result = reverse_string("hello world how are you")
print(result)