"""
Given an array of integers, write an algorithm to find the second largest element in the array. 
If the array has fewer than two elements, you should indicate that there is no second largest element.

Input: An array (or list) of integers. For example: [10, 5, 8, 12, 7]

Output: The second largest element in the array. For the example above, 
the output should be 10. If the array is [5] or [], the output should indicate that there is no second largest element.
"""

def func(arr:list):
    largest = arr[0]
    index = 0
    second=arr[0]
    second_index = 0
    if len(arr) == 0:
        print("array is empty")
        
    for i, var in enumerate(arr):
        if len(arr) < 2:
            print("there is no second largest element")
        if var > largest:
            largest = var
            index = i
    for i, var in enumerate(arr):
        if var <= largest and var >=second and i != index:
            second = var
            second_index = i
    return print(f" 2nd val: {second}. 2nd index: {second_index}.")
arr = [3,4,5,123,6,98,7,8,12,3,42]
func(arr)