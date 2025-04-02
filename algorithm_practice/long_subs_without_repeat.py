"""
Write an algorithm to find the length of the longest substring
without repeating characters in a given string.  
  
Input: "abcabcbb" Output: 3 (The longest substring without repeating characters is "abc".)
Input: "bbbbb" Output: 1 (The longest substring without repeating characters is "b".)
Input: "pwwkew" Output: 3 (The longest substring without repeating characters is "wke". 
Note that "pwwe" is a substring, but it contains repeating characters.)
Input: "" Output: 0
"""

def func(val:str):
    arr_char = []
    answer =""
    for i , element in enumerate(val):
        if element in arr_char:
            break
        else:
            arr_char.append(element)
    answer = "".join(arr_char)
    return print(f"input : {val} \noutput: {answer}")

func("abcdefghjdefdaasdewq")