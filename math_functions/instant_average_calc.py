"""
Write an algorithm to calculate the average of numbers in a list. 
Your algorithm should keep track of the sum and count of the numbers 
seen so far as it processes each number in the list.

input: func([3,4,5,6])

output:
count: 3, number list: [3]
count: 7, number list: [3, 4]
count: 12, number list: [3, 4, 5]
count: 18, number list: [3, 4, 5, 6]
last count: 18,  number list:[3, 4, 5, 6]
"""

def func(arr : list):
    element_list = []
    counter = 0
    for i, element in enumerate(arr):
        element_list.append(element)
        counter += element_list[i]
        counter / len(element_list)
        print(f"count: {counter}, number list: {element_list}")
    print(f"last count: {counter},  number list:{element_list}")
    
func([3,4,5,6,8,9,7])