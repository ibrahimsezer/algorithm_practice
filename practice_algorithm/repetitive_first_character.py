"""
Find the first character in a string (string).
If there is no repeating character, return none.

Input: "algoritma"
Output: "a"

Input: "merhaba"
Output: "a"

Input: "python"
Output: None

"""


def first_repeated_char(s):
    seen_chars = set()
    for char in s:
        if char in seen_chars:
            return char
        seen_chars.add(char)
    return None

print(first_repeated_char("helloworld"))
print(first_repeated_char("python"))
print(first_repeated_char("algorithm"))

