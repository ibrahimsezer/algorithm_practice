import numpy as np
import matplotlib.pyplot as plt
from basic_neural_network import NeuralNetwork

# --- SIMULATION LOGIC ---


def run_simulation(agent, steps=100, return_history=False, fixed_start=False):
    # Setup Scenario
    if fixed_start:
        food = 50
        temp = 25
    else:
        food = np.random.randint(30, 80)
        temp = np.random.randint(15, 30)

    alive = True
    steps_survived = 0
    total_penalty = 0

    history = {"food": [], "temp": [], "action": []}

    for _ in range(steps):
        if not alive:
            if return_history:
                # Pad with zeros for plotting
                history["food"].append(0)
                history["temp"].append(0)
                history["action"].append(0)
            continue

        steps_survived += 1

        if return_history:
            history["food"].append(food)
            history["temp"].append(temp)

        # --- IMPROVED INPUTS ---
        # 1. Food (Normalized)
        norm_food = food / 100.0
        # 2. Temperature (Normalized)
        norm_temp = temp / 50.0
        # 3. Distance from Ideal Temp (Helpful feature for AI)
        # Ideal is roughly 24. If temp is 24, diff is 0. If 10, diff is -0.5 approx.
        temp_diff = (temp - 24) / 24.0

        inputs = np.array([[norm_food, norm_temp, temp_diff]])

        # Action Decision
        output = agent.forward(inputs)
        action = np.argmax(output)

        if return_history:
            history["action"].append(action)

        # --- DYNAMICS ---
        # Reduced decay slightly to give them a chance
        food -= 1.5
        temp -= 0.3  # Slow cooling

        if action == 1:  # Eat
            food += 15
        elif action == 2:  # Heat
            temp += 5.0
            food -= 2.0  # Heating costs energy
        elif action == 3:  # Cool
            temp -= 5.0
            food -= 2.0

        food = np.clip(food, 0, 100)
        temp = np.clip(temp, -20, 60)  # Wider physical limits

        # --- NEW SCORING SYSTEM ---
        step_penalty = 0

        # Penalty 1: Hunger
        if food < 10:
            step_penalty += 50
            alive = False  # Starved
        elif food < 30:
            step_penalty += 2  # Mild hunger

        # Penalty 2: Temperature
        # Wider survival range (-5 to 45), but narrow comfort zone
        if temp < -5 or temp > 45:
            step_penalty += 50
            alive = False  # Frozen or Burned
        elif temp < 20 or temp > 28:
            step_penalty += 2  # Discomfort

        total_penalty += step_penalty

    # --- FITNESS CALCULATION ---
    # Primary Goal: Stay alive as long as possible (steps_survived)
    # Secondary Goal: Minimize penalty (discomfort)
    # We square steps_survived to reward living longer exponentially
    fitness = (steps_survived**2) - (total_penalty * 2)

    return fitness, steps_survived, history


# --- GENETIC ALGORITHM ---


def crossover(parent1, parent2):
    child = NeuralNetwork(input_size=3)  # Remember input size is 3 now
    child.W1 = (parent1.W1 + parent2.W1) / 2
    child.W2 = (parent1.W2 + parent2.W2) / 2
    child.W3 = (parent1.W3 + parent2.W3) / 2
    return child


def mutate(agent, rate=0.2, intensity=0.5):
    if np.random.rand() < rate:
        agent.W1 += np.random.randn(*agent.W1.shape) * intensity
    if np.random.rand() < rate:
        agent.W3 += np.random.randn(*agent.W3.shape) * intensity


# --- MAIN ---

POP_SIZE = 50
GENERATIONS = 100
population = [NeuralNetwork(input_size=3) for _ in range(POP_SIZE)]
survival_log = []

print("--- Starting Improved Evolution ---")

for gen in range(GENERATIONS):
    scores = []

    for agent in population:
        fit, survived, _ = run_simulation(agent, steps=100)
        scores.append((fit, survived, agent))

    scores.sort(key=lambda x: x[0], reverse=True)

    best_survival = scores[0][1]
    survival_log.append(best_survival)

    if gen % 10 == 0:
        print(f"Gen {gen}: Max Steps Survived = {best_survival}/100")

    # Elitism
    new_population = [x[2] for x in scores[:10]]

    while len(new_population) < POP_SIZE:
        # Tournament Selection (Pick random 5, take best)
        # This helps maintain diversity better than just picking top 10
        candidates = [scores[np.random.randint(0, POP_SIZE)] for _ in range(5)]
        candidates.sort(key=lambda x: x[0], reverse=True)
        parent1 = candidates[0][2]

        candidates = [scores[np.random.randint(0, POP_SIZE)] for _ in range(5)]
        candidates.sort(key=lambda x: x[0], reverse=True)
        parent2 = candidates[0][2]

        child = crossover(parent1, parent2)
        mutate(child, rate=0.3, intensity=0.6)  # High mutation initially
        new_population.append(child)

    population = new_population

# --- VISUALIZATION ---
best_agent = population[0]
_, _, history = run_simulation(
    best_agent, steps=100, return_history=True, fixed_start=True
)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Graph 1: Survival Time
ax1.plot(survival_log, color="blue", linewidth=2)
ax1.set_title("Evolution of Survival Capability")
ax1.set_ylabel("Steps Survived (Max 100)")
ax1.set_xlabel("Generation")
ax1.grid(True)

# Graph 2: Strategy
steps = range(len(history["food"]))
ax2.plot(steps, history["food"], label="Food", color="green")
ax2.plot(steps, history["temp"], label="Temp", color="red")

# Ideal Zones
ax2.axhspan(20, 28, color="orange", alpha=0.15, label="Comfort Zone")
ax2.axhspan(0, 10, color="black", alpha=0.1, label="Danger Zone")
ax2.axhline(y=50, color="green", linestyle="--")

# Actions
actions = np.array(history["action"])
ax2.scatter(
    np.where(actions == 1)[0],
    [history["food"][i] for i in np.where(actions == 1)[0]],
    c="lime",
    marker="^",
    label="Eat",
)
ax2.scatter(
    np.where(actions == 2)[0],
    [history["temp"][i] for i in np.where(actions == 2)[0]],
    c="darkred",
    marker="^",
    label="Heat",
)
ax2.scatter(
    np.where(actions == 3)[0],
    [history["temp"][i] for i in np.where(actions == 3)[0]],
    c="blue",
    marker="v",
    label="Cool",
)

ax2.set_title("Best Agent Behavior")
ax2.legend(loc="upper right")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
