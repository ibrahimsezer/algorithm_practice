"""
The Fibonacci sequence is a sequence in which each term is the sum of two preceding terms.
F(n)=F(n−1)+F(n−2),F(0)=0,F(1)=1
"""

def fibonacci(n):
    a,b = 0,1
    for i in range(n):
        a,b = b, a+b
    return a

print(fibonacci(10))