# Algorithm Practice Collection

A collection of Python, Dart implementations for common algorithmic problems and mathematical functions.

## Implemented Algorithms

### Algorithm Practice

Located in `algorithm_practice/`

1. **Kadane's Algorithm** (`kadane_algorithm.py`)
   - Finds the contiguous subarray with the maximum sum
   - Returns both the maximum sum and the start/end indices
   - Time Complexity: O(n)

2. **Longest Common Prefix** (`longest_common_prefix.py`)
   - Finds the longest common prefix shared by all strings in an array
   - Returns empty string if no common prefix exists
   - Time Complexity: O(S) where S is the sum of all characters in all strings

3. **First Repeated Character** (`repetitive_first_character.py`)
   - Finds the first repeating character in a string
   - Returns None if no character repeats
   - Time Complexity: O(n²)

4. **Second Largest Element** (`second_largest_element.py`)
   - Finds the second largest element in an array of integers
   - Handles edge cases like empty arrays or arrays with less than 2 elements
   - Time Complexity: O(n)

5. **Longest Substring Without Repeat** (`long_subs_without_repeat.py`)
   - Finds the length of the longest substring without repeating characters
   - Returns the substring and its length
   - Time Complexity: O(n)

6. **Reverse String** (`reverse_string.py`)
   - Reverses the order of words in a given string
   - Preserves word order while reversing the overall string
   - Time Complexity: O(n)

### Mathematical Functions

Located in `math_functions/`

1. **Fibonacci Sequence** (`fibonacci.py`)
   - Implements the Fibonacci sequence generator
   - F(n) = F(n-1) + F(n-2), where F(0)=0, F(1)=1
   - Time Complexity: O(n)

2. **Primality Test** (`primality_test.py`)
   - Checks if a given number is prime
   - Uses optimized square root method
   - Time Complexity: O(√n)

3. **Euclidean Algorithm** (`euclidean_algorithm.py`)
   - Finds the Greatest Common Divisor (GCD) of two numbers
   - Uses the Euclidean algorithm method
   - Time Complexity: O(log min(a,b))

### Object-Oriented Programming Practice

Located in `oop_practice/`

1. **Exercise** (`exercise.dart`)
   - Contains Dart implementations of OOP concepts
   - Includes various class and object examples

### Neural Networks & Genetic Algorithms

Located in `neural_networks/`

1. **Basic Neural Network** (`basic_neural_network.py`)
   - Basic implementation of a Multi-Layer Perceptron (MLP)
   - Demonstrates forward propagation and decision boundaries

2. **XOR Problem Solver** (`xor_problem_with_ga.py`)
   - Solves the XOR logical problem using Neuro-Evolution
   - Uses Genetic Algorithm instead of Backpropagation for weight optimization

3. **Survival Simulation** (`survival_with_ga.py`)
   - Autonomous agent simulation managing vital signs (Hunger, Temperature)
   - Evolves survival strategies over generations using Genetic Algorithms
   - Includes visualization of evolutionary progress and agent behavior

4. **Lunar Lander** (`lunar_lander/`)
   - Implementation of a Lunar Lander control problem
   - Uses Neural Networks to control thrusters for safe landing

## Usage

Each algorithm is implemented in its own file. To use any algorithm:

1. Import the specific file
2. Call the corresponding function with appropriate parameters

## Requirements

- Python 3.x (for Python files)
- Dart SDK (for Dart files)

## Testing

Each file includes example test cases and print statements demonstrating usage.

## Project Structure

```
python_function/
├── algorithm_practice/
│   ├── kadane_algorithm.py
│   ├── longest_common_prefix.py
│   ├── repetitive_first_character.py
│   ├── second_largest_element.py
│   ├── long_subs_without_repeat.py
│   └── reverse_string.py
├── math_functions/
│   ├── fibonacci.py
│   ├── primality_test.py
│   └── euclidean_algorithm.py
├── neural_networks/
│   ├── lunar_lander/
│   ├── basic_neural_network.py
│   ├── survival_with_ga.py
│   └── xor_problem_with_ga.py
└── oop_practice/
    └── exercise.dart
```
