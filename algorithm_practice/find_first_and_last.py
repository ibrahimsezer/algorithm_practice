"""
Problem: Given a sorted array of integers (sorted in ascending order), find the first and last position of a given target integer in the array. If the target is not found in the array, return [-1, -1].

Examples:

Input array: [5, 7, 7, 8, 8, 10], Target number: 8
Expected output: [3, 4] (The number 8 first appears at index 3 and last appears at index 4)

Input array: [5, 7, 7, 8, 8, 10], Target number: 6
Expected output: [-1, -1] (The number 6 is not found in the array)

Input array: [], Target number: 0
Expected output: [-1, -1] (The array is empty)
"""

def func(arr: list, target: int):
    first_index = -1
    last_index  = -1
    for i,element in enumerate(arr):
        if target == element and first_index == -1:
            first_index  = i
        elif target == element and (last_index <=i):
            last_index = i
    return [first_index,last_index]
    #print(f"target:{target}, first_index:{first_index}, last_index:{last_index}")
    
func([3,4,5,7,7,78], 7)


