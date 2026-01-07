import numpy as np
import matplotlib.pyplot as plt
from basic_neural_network import NeuralNetwork

# --- 2. SIMULATION LOGIC (HARDER MODE) ---


def run_simulation(agent, steps=50, return_history=False, fixed_start=False):
    """
    Runs the survival simulation.
    Now includes 'Natural Decay' to force the agent to act.
    """

    # Initialization
    # If fixed_start is True (for final plotting), give a challenging start
    if fixed_start:
        food = 40  # Slightly hungry
        temp = 22  # Good temp, but will drop fast
    else:
        # Random start for training
        food = np.random.randint(30, 80)
        temp = np.random.randint(15, 30)

    total_penalty = 0
    alive = True

    history = {"food": [], "temp": [], "action": []}

    for _ in range(steps):
        if not alive:
            # If dead, fill the rest of the history with 0s for easier plotting
            if return_history:
                history["food"].append(0)
                history["temp"].append(0)
                history["action"].append(0)
            continue

        # Record inputs for plotting
        if return_history:
            history["food"].append(food)
            history["temp"].append(temp)

        # 1. Normalize Input (0-1)
        inputs = np.array([[food / 100.0, temp / 50.0]])

        # 2. Get Action
        output = agent.forward(inputs)
        action = np.argmax(output)

        if return_history:
            history["action"].append(action)

        # --- KEY CHANGE: ENVIRONMENT DYNAMICS ---

        # Natural decay (Entropy)
        food -= 2.0  # Metabolism: Getting hungry automatically
        temp -= 0.5  # Cooling: Environment gets colder naturally!

        # 3. Apply Action Effects
        if action == 0:  # Wait
            pass  # Saves energy, but temp still drops due to environment
        elif action == 1:  # Eat
            food += 15
        elif action == 2:  # Heat Up
            temp += 4.0  # Fighting the cold
            food -= 1.0  # Heating takes energy
        elif action == 3:  # Cool Down
            temp -= 4.0
            food -= 1.0  # Cooling takes energy

        # Clamp values
        food = np.clip(food, 0, 100)
        temp = np.clip(temp, -10, 60)

        # --- 4. CALCULATE PENALTIES ---
        step_penalty = 0

        # Rule 1: Hunger
        if food < 15:
            step_penalty += 1000  # High penalty for starvation risk
            alive = False
        elif food < 50:
            step_penalty += 5  # Mild hunger penalty

        # Rule 2: Temperature (Ideal: 20-28)
        if temp < 18 or temp > 30:  # Expanded danger zone slightly
            step_penalty += 1000  # High penalty for freezing/burning
            alive = False
        elif temp < 20 or temp > 28:
            step_penalty += 5  # Discomfort penalty

        total_penalty += step_penalty

    fitness = 1 / (total_penalty + 1)
    return fitness, total_penalty, history


# --- 3. GENETIC ALGORITHM ---


def crossover(parent1, parent2):
    child = NeuralNetwork()
    child.W1 = (parent1.W1 + parent2.W1) / 2
    child.W2 = (parent1.W2 + parent2.W2) / 2
    child.W3 = (parent1.W3 + parent2.W3) / 2
    return child


def mutate(agent, rate=0.1):
    if np.random.rand() < rate:
        agent.W1 += np.random.randn(*agent.W1.shape) * 0.5
    if np.random.rand() < rate:
        agent.W3 += np.random.randn(*agent.W3.shape) * 0.5


# --- 4. MAIN EXECUTION ---

POP_SIZE = 50
GENERATIONS = 150  # Increased generations for harder task
population = [NeuralNetwork() for _ in range(POP_SIZE)]
best_penalties_log = []

print("--- Starting Evolution (Hard Mode) ---")

for gen in range(GENERATIONS):
    scores = []

    for agent in population:
        # Run simulation
        fit, penalty, _ = run_simulation(agent)
        scores.append((fit, penalty, agent))

    scores.sort(key=lambda x: x[0], reverse=True)
    best_penalty = scores[0][1]
    best_penalties_log.append(best_penalty)

    if gen % 10 == 0:
        print(f"Gen {gen}: Best Penalty = {best_penalty:.1f}")

    # Reproduction
    new_population = [x[2] for x in scores[:5]]  # Keep top 5

    while len(new_population) < POP_SIZE:
        parent1 = scores[np.random.randint(0, 15)][2]  # Select from top 15
        parent2 = scores[np.random.randint(0, 15)][2]

        child = crossover(parent1, parent2)
        mutate(child, rate=0.15)
        new_population.append(child)

    population = new_population

print("--- Evolution Completed ---")

# --- 5. VISUALIZATION ---

best_agent = population[0]
# Use fixed_start=True to test a standard scenario, not random
_, final_penalty, history = run_simulation(
    best_agent, steps=100, return_history=True, fixed_start=True
)

# Create Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Plot 1: Training Logic
ax1.plot(best_penalties_log, color="blue")
ax1.set_title("Training Progress (Lower Penalty is Better)")
ax1.set_ylabel("Penalty")
ax1.set_xlabel("Generation")
ax1.grid(True)

# Plot 2: Simulation Details
time_steps = range(len(history["food"]))
ax2.plot(time_steps, history["food"], label="Food (Green)", color="green", linewidth=2)
ax2.plot(time_steps, history["temp"], label="Temp (Red)", color="red", linewidth=2)

# Add Threshold Zones
ax2.axhspan(20, 28, color="orange", alpha=0.1, label="Ideal Temp Zone")
ax2.axhspan(0, 15, color="black", alpha=0.1, label="Starvation Zone")
ax2.axhline(y=50, color="green", linestyle="--", alpha=0.5, label="Hunger Threshold")

# Mark Actions on the Graph to see what happened
actions = np.array(history["action"])
eat_indices = np.where(actions == 1)[0]
heat_indices = np.where(actions == 2)[0]
cool_indices = np.where(actions == 3)[0]

ax2.scatter(
    eat_indices,
    [history["food"][i] for i in eat_indices],
    color="lime",
    marker="^",
    zorder=5,
    label="Action: Eat",
)
ax2.scatter(
    heat_indices,
    [history["temp"][i] for i in heat_indices],
    color="darkred",
    marker="^",
    zorder=5,
    label="Action: Heat",
)
ax2.scatter(
    cool_indices,
    [history["temp"][i] for i in cool_indices],
    color="blue",
    marker="v",
    zorder=5,
    label="Action: Cool",
)

ax2.set_title("Agent Survival Strategy (Triangle = Action Taken)")
ax2.set_xlabel("Time Step")
ax2.set_ylabel("Value")
ax2.legend(loc="upper right", bbox_to_anchor=(1.1, 1))
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
