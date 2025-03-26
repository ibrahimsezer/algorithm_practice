# Algorithm Practice Collection

A collection of Python implementations for common algorithmic problems.

## Implemented Algorithms

### 1. Kadane's Algorithm
Located in `kadane_algorithm.py`
- Finds the contiguous subarray with the maximum sum
- Returns both the maximum sum and the start/end indices
- Time Complexity: O(n)

Example:
```python
Input: [-33, -11, 5, -4, 9]
Output: sum => start : end
```

### 2. Longest Common Prefix
Located in `longest_common_prefix.py`
- Finds the longest common prefix shared by all strings in an array
- Returns empty string if no common prefix exists
- Time Complexity: O(S) where S is the sum of all characters in all strings

Example:
```python
Input: ["flower", "flow", "flight"]
Output: "fl"
```

### 3. First Repeated Character
Located in `repetitive_first_character.py`
- Finds the first repeating character in a string
- Returns None if no character repeats
- Time Complexity: O(n²)

Example:
```python
Input: "helloworld"
Output: "l"
```

## Usage

Each algorithm is implemented in its own Python file. To use any algorithm:

1. Import the specific file
2. Call the corresponding function:
   - `kadane(arr)` for maximum subarray sum
   - `longest_common_prefix(arr)` for common prefix
   - `first_repeated_char(s)` for first repeated character

## Requirements
- Python 3.x

## Testing
Each file includes example test cases in the comments and a print statement demonstrating usage.

## Project Structure
      |-algorithm_practice
         ├── kadane_algorithm.py
         ├── longest_common_prefix.py
         └── repetitive_first_character.py