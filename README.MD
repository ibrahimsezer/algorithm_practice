# Algorithm Practice Collection

A collection of Python and Dart implementations for common algorithmic problems, mathematical functions, and **Advanced Neural Network Simulations**.

---

## 🧠 Neural Networks & Artificial Intelligence

This project contains a growing collection of AI implementations, ranging from basic algorithms to complex evolutionary simulations.

### 1. Basic Neural Network Laboratory (✨ NEW & UPGRADE)

**Location:** `neural_networks/basic_nn/`

![Basic Neural Network Laboratory](https://raw.githubusercontent.com/ibrahimsezer/algorithm_practice/refs/heads/main/neural_networks/basic_nn/figure_basic_nn_1.png)

An interactive educational tool to visualize how Deep Neural Networks learn. It allows you to drag a race car (the AI) between "Evolution" and "Gradient Descent".

#### Key Features

* **Dual Learning Strategies**:
  * **Backpropagation (Gradient Descent)**: Uses Calculus to mathematically optimize weights closer to the target (Fast & Precise).
  * **Genetic Mutation (Evolution)**: Randomly modifies weights to "explore" new solutions (Chaotic & Creative).
* **Dynamic Architecture**: The `NeuralNetwork` class (`brain.py`) supports any list-based layer structure (e.g., `[2, 8, 8, 1]`).
* **Real-time Visualization**:
  * **Decision Boundary**: A Heatmap showing the AI's "World View" (`laboratory.py`).
  * **Network Anatomy**: Visualizes neurons, layers, and connection weights.

#### 📊 System Architecture

```mermaid
graph TD
    User([User]) -->|Click 'Train'| Backprop[Backpropagation (Gradient Descent)]
    User -->|Click 'Mutate'| Genetic[Genetic Mutation (Random Walk)]
    
    Backprop -->|Update Weights| Brain[NeuralNetwork Class (brain.py)]
    Genetic -->|Update Weights| Brain
    
    Brain -->|Forward Pass| Prediction
    
    subgraph Visualization [Matplotlib Loop]
        Decision[Decision Boundary Map]
        Structure[Network Anatomy]
    end
    
    Brain -.-> Visualization
    Visualization ==>|Visual Feedback| User
```

#### How to Run

```bash
python neural_networks/basic_nn/experiment_table.py
```

---

### 2. Survival Simulation (Modular Genetic Algorithm)

**Location:** `neural_networks/survival_ga/`

A complex simulation where autonomous agents struggle to survive in a hostile environment. They must balance hunger and temperature, learning strategies over generations.

* **Modules**: `brain.py` (Logic), `simulation.py` (Environment), `main.py` (Runner).

---

### 3. Legacy Implementations

* **Lunar Lander**: `neural_networks/lunar_lander/` - Control logic for landing.
* **XOR Solver**: `neural_networks/xor_problem_with_ga.py` - Early genetic algorithm test.

---

## 📂 Project Structure

```text
python_function/
├── algorithm_practice/         # Common coding interview problems
│   ├── kadane_algorithm.py
│   ├── longest_common_prefix.py
│   ├── repetitive_first_character.py
│   ├── second_largest_element.py
│   ├── long_subs_without_repeat.py
│   └── reverse_string.py
├── math_functions/             # Pure mathematical algorithms
│   ├── fibonacci.py
│   ├── primality_test.py
│   └── euclidean_algorithm.py
├── neural_networks/            # AI & Machine Learning
│   ├── basic_nn/               # [ACTIVE] Deep Learning Lab
│   │   ├── brain.py            # Neural Network Class (Backprop + GA)
│   │   ├── laboratory.py       # Visualization Utils
│   │   └── experiment_table.py # Interactive Runner
│   ├── survival_ga/            # [ACTIVE] Survival Simulation
│   │   ├── main.py
│   │   ├── brain.py
│   │   └── simulation.py
│   ├── lunar_lander/           # Lunar Lander Control
│   └── basic_neural_network.py # Legacy MLP
└── oop_practice/               # Object Oriented Design
    └── exercise.dart
```

---

## 💻 Implemented Algorithms (Classic)

### Algorithm Practice

* **Kadane's Algorithm**: O(n) Maximum Subarray Sum.
* **Longest Common Prefix**: O(S) String manipulation.
* **First Repeated Character**: O(n²) Search.
* **Second Largest Element**: O(n) Array traversal.
* **Longest Substring Without Repeat**: O(n) Sliding Window.
* **Reverse String**: O(n) In-place reversal.

### Mathematical Functions

* **Fibonacci**: O(n) Sequence generation.
* **Primality Test**: O(√n) Math optimization.
* **Euclidean Algorithm**: O(log min(a,b)) GCD calculation.

## Requirements

* **Python 3.x**: `numpy`, `matplotlib`
* **Dart SDK**: (For OOP practice files)
