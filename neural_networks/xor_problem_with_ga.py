import numpy as np
from basic_neural_network import NeuralNetwork

# --- GENETIC ALGORITHM FUNCTIONS ---


def calculate_fitness(nn):
    """
    Measures the XOR performance of the network.
    The lower the error, the higher the Fitness (Score).
    """
    X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_target = np.array([[0], [1], [1], [0]])

    predictions = nn.forward(X_xor)
    mse = np.mean((y_target - predictions) ** 2)  # Mean Squared Error
    return 1 / (mse + 1e-9)  # Avoid division by zero if error is 0


def mutate(nn, mutation_rate=0.1, strength=0.5):
    """
    Adds random noise to the network's weights.
    """
    parameters = [nn.W1, nn.b1, nn.W2, nn.b2, nn.W3, nn.b3]

    for param in parameters:
        if np.random.rand() < mutation_rate:
            # Add random noise
            noise = np.random.randn(*param.shape) * strength
            param += noise


def crossover(parent1, parent2):
    """
    Produces a child by taking the average of two parents' weights.
    """
    child = NeuralNetwork()
    child.W1 = (parent1.W1 + parent2.W1) / 2
    child.b1 = (parent1.b1 + parent2.b1) / 2
    child.W2 = (parent1.W2 + parent2.W2) / 2
    child.b2 = (parent1.b2 + parent2.b2) / 2
    child.W3 = (parent1.W3 + parent2.W3) / 2
    child.b3 = (parent1.b3 + parent2.b3) / 2
    return child


# --- MAIN LOOP ---

# 1. Initial Population
population_size = 50
population = [NeuralNetwork() for _ in range(population_size)]
generation_count = 1000

print("Evolution starting...")

for gen in range(generation_count):
    # 2. Calculate scores for everyone and sort (Highest score first)
    population = sorted(population, key=lambda x: calculate_fitness(x), reverse=True)

    best_individual = population[0]
    best_error = 1 / calculate_fitness(best_individual)

    if gen % 100 == 0:
        print(f"Gen {gen}: Lowest Error (MSE): {best_error:.5f}")
        # Early exit if error is low enough
        if best_error < 0.001:
            print("Solution found!")
            break

    # 3. Create New Generation (Elitism + Crossover)
    new_population = []

    # Carry over the top 5 individuals directly (Elitism)
    new_population.extend(population[:5])

    # Fill the remaining 45 by breeding from the top performers
    while len(new_population) < population_size:
        # Select 2 parents randomly from the top 20%
        parent1 = population[np.random.randint(0, 10)]
        parent2 = population[np.random.randint(0, 10)]

        child = crossover(parent1, parent2)
        mutate(child, mutation_rate=0.3, strength=0.2)
        new_population.append(child)

    population = new_population

# --- FINAL TEST ---
print("\n--- Training Complete ---")
X_test = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
result = population[0].forward(X_test)

print("XOR Inputs:")
print(X_test)
print("Trained Network Predictions:")
print(np.round(result, 3))
