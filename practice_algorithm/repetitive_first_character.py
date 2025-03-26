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
    for i in range(len(s)):
        current_char = s[i]
        for j in range(i+1,len(s)):
            if current_char == s[j]:
                return current_char
    return None


print(first_repeated_char("helloworld"))
print(first_repeated_char("python"))
print(first_repeated_char("algorithm"))


