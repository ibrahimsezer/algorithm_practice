"""
 You are given a list of positive integers. Write an algorithm to find all possible pairs of numbers in the list that sum up to a specific target number. The order of the numbers in a pair does not matter (i.e., (3, 5) and (5, 3) are considered the same pair). Also, consider cases where the same number can be used twice in a pair (e.g., (5, 5) if the target is 10).

For example, if the list is [1, 2, 3, 4, 5, 6] and the target number is 7, your algorithm should find the following pairs:

(1, 6)
(2, 5)
(3, 4)
As another example, if the list is [2, 3, 4, 5] and the target number is 6, your algorithm should find the following pairs:

(2, 4)
(3, 3)
Your algorithm should return all the found pairs in a list or a similar data structure.
"""

def func(arr:list, target:int):
    possible_list =[]
    seen_pairs = set()
    for i,var_i in enumerate(arr):
        for j,var_j in enumerate(arr):
            if var_i + var_j == target:
                pair = tuple(sorted((var_i,var_j)))
                if pair not in seen_pairs:
                    possible_list.append([var_i,var_j])
                    seen_pairs.add(pair)
    return possible_list
arr = [1,2,3,4,5]
TARGET = 6
result = func(arr,TARGET)
print(result)