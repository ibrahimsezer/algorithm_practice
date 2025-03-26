"""
Given an array of lowercase strings, write a function to find the longest common prefix shared by all the strings.

If no common prefix exists, return an empty string ("").

Input: ["flower", "flow", "flight"]
Output: "fl"

Input: ["dog", "racecar", "car"]
Output: ""

Input: ["interspecies", "interstellar", "interstate"]
Output: "inters"

Input: ["apple", "app", "application"]
Output: "app"

"""

def longest_common_prefix(arr):
    if not arr:
        return ""
    min_len = len(arr[0])
    for word in arr:
        min_len = min(min_len, len(word))
    
    for i in range(min_len):
        current_char = arr[0][i]
        
        for word in arr:
            if word[i] != current_char:
                return arr[0][:i]
    return arr[0][:min_len]

print(longest_common_prefix(["apple","app","application"]))