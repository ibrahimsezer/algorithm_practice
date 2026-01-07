import numpy as np
from basic_neural_network import NeuralNetwork

# --- 2. SIMULATION AND FITNESS FUNCTION ---


def run_simulation(agent):
    """
    Simulates a life cycle (e.g., 50 steps/hours) for an agent.
    Calculates penalty points based on defined rules.
    """
    # Initial State (Randomized to prevent memorization)
    food = np.random.randint(40, 70)
    temperature = np.random.randint(15, 30)

    total_penalty = 0
    is_alive = True

    # Simulation duration (Number of steps)
    for step in range(50):
        if not is_alive:
            break

        # 1. Agent perceives the state (Input)
        # Normalizing data (scaling between 0-1) makes learning easier
        input_data = np.array([[food / 100.0, temperature / 50.0]])

        # 2. Agent makes a decision (Output)
        decisions = agent.forward(input_data)
        selected_action = np.argmax(
            decisions
        )  # Index of the neuron with the highest value

        # 3. Apply Action and Natural Consumption
        # Food decreases slightly each step (Metabolism)
        food -= 3

        if selected_action == 0:  # Wait
            pass
        elif selected_action == 1:  # Eat
            food += 15
        elif selected_action == 2:  # Warm Up
            temperature += 4
        elif selected_action == 3:  # Cool Down
            temperature -= 4

        # Maintain food limits (between 0-100)
        food = np.clip(food, 0, 100)

        # --- 4. DEFINED RULES (PENALTY POINTS) ---

        # RULE 1: Food Control
        if food >= 50:
            total_penalty += 0  # No problem
        elif 15 <= food < 50:
            total_penalty += 10  # Mild hunger
        else:  # food < 15
            total_penalty += 5000  # Fatal hunger
            is_alive = False  # Consider dead or penalize heavily

        # RULE 2: Temperature Control
        # Target: between 20-28
        if 20 <= temperature <= 28:
            total_penalty += 0  # Ideal
        elif (15 <= temperature < 20) or (28 < temperature <= 33):
            # +- 5 degree deviation
            total_penalty += 10
        else:
            # Greater difference (Too cold or too hot)
            total_penalty += 7000
            is_alive = False

    # Fitness Score: The lower the penalty, the higher the score.
    # Establishing inverse proportion.
    fitness = 1 / (total_penalty + 1)
    return fitness, total_penalty


# --- 3. GENETIC ALGORITHM LOOP ---


def crossover(parent1, parent2):
    child = NeuralNetwork(input_size=2, hidden_size=8, output_size=4)
    # Take the average of weights
    child.W1 = (parent1.W1 + parent2.W1) / 2
    child.W2 = (parent1.W2 + parent2.W2) / 2
    child.W3 = (parent1.W3 + parent2.W3) / 2
    return child


def mutation(agent, rate=0.1):
    if np.random.rand() < rate:
        agent.W1 += np.random.randn(*agent.W1.shape) * 0.5
    if np.random.rand() < rate:
        agent.W3 += np.random.randn(*agent.W3.shape) * 0.5


# Create Population
pop_size = 20
population = [
    NeuralNetwork(input_size=2, hidden_size=8, output_size=4) for _ in range(pop_size)
]

print("Training Started... (Goal: Bring penalty close to 0)")

for generation in range(100):  # Train for 100 generations
    scores = []

    # Test each agent
    for agent in population:
        fit, penalty = run_simulation(agent)
        scores.append((fit, penalty, agent))

    # Sort by fitness (Highest fitness is best)
    scores.sort(key=lambda x: x[0], reverse=True)

    best_penalty = scores[0][1]

    if generation % 10 == 0:
        print(f"Generation {generation}: Lowest penalty score: {best_penalty}")
        if best_penalty < 50:
            print("Agent learned to survive!")

    # Create new generation (Elitism: Keep the best 4 agents)
    new_pop = [x[2] for x in scores[:4]]

    while len(new_pop) < pop_size:
        # Select parents from the top 10
        parent1 = scores[np.random.randint(0, 10)][2]
        parent2 = scores[np.random.randint(0, 10)][2]

        child = crossover(parent1, parent2)
        mutation(child)
        new_pop.append(child)

    population = new_pop

# --- 4. RESULT TEST ---
print("\n--- Best Agent Test ---")
best_agent = population[0]
food_val = 45  # Risky start (below 50)
temp_val = 30  # Risky start (above 28)

print(f"Start -> Food: {food_val}, Temperature: {temp_val}")
input_data = np.array([[food_val / 100.0, temp_val / 50.0]])
decision = np.argmax(best_agent.forward(input_data))

actions = ["Wait", "Eat (+Food)", "Warm Up (+Temperature)", "Cool Down (-Temperature)"]
print(f"AI Decision: {actions[decision]}")
