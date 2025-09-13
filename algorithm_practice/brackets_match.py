
stack = []
value = input("Enter a value (or 'exit' to quit): ")

for i in range(len(value)):
    if value[i] == '(' or value[i] == '{' or value[i] == '[':
        stack.append(value[i])
    elif value[i] == ')' or value[i] == '}' or value[i] == ']':
        if not stack:
            print("Unmatched closing bracket found.")
            break
        top = stack.pop()
        if (top == '(' and value[i] != ')') or (top == '{' and value[i] != '}') or (top == '[' and value[i] != ']'):
            print("Mismatched brackets found.")
            break
        else:
            print("Brackets are balanced.")
