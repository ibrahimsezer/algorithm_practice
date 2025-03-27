"""
    This algorithm is used to find the greatest common divisor of two numbers.
    a:256 b:192
    
"""

def euclidean(a,b):
    while b!=0:
        a,b = b, a%b
        print((f"a: {a} | b: {b}"))
        
    return (f"\ngreatest common divisor is {a}")
print(euclidean(8,24))