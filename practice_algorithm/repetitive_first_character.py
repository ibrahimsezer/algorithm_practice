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

