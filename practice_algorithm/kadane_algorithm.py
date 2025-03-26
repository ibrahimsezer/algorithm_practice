"""
Given an array arr[], the task is to find the subarray
that has the maximum sum and return its sum.

Examples:

Input: arr[] = {2, 3, -8, 7, -1, 2, 3}
Output: 11
Explanation: The subarray {7, -1, 2, 3} has the largest sum 11.


Input: arr[] = {-2, -4}
Output: –2
Explanation: The subarray {-2} has the largest sum -2.


Input: arr[] = {5, 4, 1, 7, 8}
Output: 25
Explanation: The subarray {5, 4, 1, 7, 8} has the largest sum 25.

"""
def kadane(arr):
    if len(arr) ==0:
        return 0
    
    max_sum = arr[0]
    current_sum = arr[0]

    for i in range(1,len(arr)):
        current_element = arr[i]
        
        if current_sum + current_element> current_element:
            current_sum = current_sum + current_element
        else:
            current_sum = current_element
        
        if current_sum > max_sum:
            max_sum = current_sum
    return max_sum
    
print(kadane([-33,-11,5,-4,9]))