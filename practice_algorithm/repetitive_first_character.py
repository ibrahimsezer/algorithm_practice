input = "helloworld"
seen_chars = set()

for char in input:
    if char in seen_chars:
        print(f"first character: {char}")
        break
    seen_chars.add(char)