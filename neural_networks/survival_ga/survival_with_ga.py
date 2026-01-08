import numpy as np
import matplotlib.pyplot as plt
import copy

# --- CONFIGURATION (SİMÜLASYON AYARLARI) ---
# Magic numbers'ı tek bir yerden yönetiyoruz.
CONFIG = {
    "input_size": 3,  # Inputs: Food, Temp, Temp_Diff
    "hidden_size": 3,
    "output_size": 4,  # Actions: Wait, Eat, Heat, Cool
    "max_food": 100,
    "start_food_min": 40,
    "start_food_max": 70,
    "start_temp_min": 15,
    "start_temp_max": 30,
    "decay_food": 6.0,  # Metabolic cost per turn
    "decay_temp": 1.5,  # Natural cooling per turn
    "action_eat_gain": 7.0,
    "action_heat_val": 5.0,
    "action_cool_val": 5.0,
    "action_energy_cost": 3.0,  # Cost of Heating/Cooling
    "limit_starvation": 15,  # Death below this
    "limit_freeze": -5,  # Death below this
    "limit_burn": 45,  # Death above this
    "ideal_temp_min": 20,
    "ideal_temp_max": 28,
    "ideal_food_min": 50,
}


# --- 1. THE BRAIN (Neural Network) ---
class Brain:
    def __init__(self):
        self.W1 = np.random.randn(CONFIG["input_size"], CONFIG["hidden_size"])
        self.b1 = np.zeros((1, CONFIG["hidden_size"]))
        self.W2 = np.random.randn(CONFIG["hidden_size"], CONFIG["hidden_size"])
        self.b2 = np.zeros((1, CONFIG["hidden_size"]))
        self.W3 = np.random.randn(CONFIG["hidden_size"], CONFIG["output_size"])
        self.b3 = np.zeros((1, CONFIG["output_size"]))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def decide(self, inputs):
        # Forward propagation
        z1 = np.dot(inputs, self.W1) + self.b1
        a1 = self.sigmoid(z1)
        z2 = np.dot(a1, self.W2) + self.b2
        a2 = self.sigmoid(z2)
        z3 = np.dot(a2, self.W3) + self.b3
        output = self.sigmoid(z3)
        return np.argmax(output)  # Returns index of best action


# --- 2. THE ENVIRONMENT (Physics & Rules) ---
class SurvivalSimulation:
    def __init__(self, brain, fixed_start=False):
        self.brain = brain
        self.alive = True
        self.steps_survived = 0
        self.total_penalty = 0
        self.history = {"food": [], "temp": [], "action": []}

        # Initialize State
        if fixed_start:
            self.food = 50.0
            self.temp = 25.0
        else:
            self.food = float(
                np.random.randint(CONFIG["start_food_min"], CONFIG["start_food_max"])
            )
            self.temp = float(
                np.random.randint(CONFIG["start_temp_min"], CONFIG["start_temp_max"])
            )

    def get_inputs(self):
        # Normalize inputs for the brain
        norm_food = self.food / CONFIG["max_food"]
        norm_temp = self.temp / 50.0
        # Feature Engineering: Distance from ideal center (approx 24)
        ideal_center = (CONFIG["ideal_temp_max"] + CONFIG["ideal_temp_min"]) / 2
        temp_diff = (self.temp - ideal_center) / 24.0

        return np.array([[norm_food, norm_temp, temp_diff]])

    def step(self):
        if not self.alive:
            return False

        # 1. Get Decision
        inputs = self.get_inputs()
        action = self.brain.decide(inputs)
        action_limit = 1

        # 2. Record History
        self.history["food"].append(self.food)
        self.history["temp"].append(self.temp)
        self.history["action"].append(action)

        # 3. Apply Entropy (Natural Decay)
        self.food -= CONFIG["decay_food"]
        self.temp -= CONFIG["decay_temp"]

        # 4. Apply Action
        if action_limit == 0:
            action = 0
        if action == 0:  # Wait
            pass
        elif action == 1:  # Eat
            self.food += CONFIG["action_eat_gain"]
            action_limit -= 1
        elif action == 2:  # Heat
            self.temp += CONFIG["action_heat_val"]
            self.food -= CONFIG["action_energy_cost"]
            action_limit -= 1
        elif action == 3:  # Cool
            self.temp -= CONFIG["action_cool_val"]
            self.food -= CONFIG["action_energy_cost"]
            action_limit -= 1

        # 5. Physics Clamping
        self.food = np.clip(self.food, 0, CONFIG["max_food"])
        self.temp = np.clip(self.temp, -20, 60)

        # 6. Check Life/Death & Calc Penalty
        self.check_vital_signs()

        self.steps_survived += 1
        return self.alive

    def check_vital_signs(self):
        penalty = 0

        # Food Check
        if self.food < CONFIG["limit_starvation"]:
            self.alive = False
            penalty += 100  # Heavy death penalty
        elif self.food < CONFIG["ideal_food_min"]:
            penalty += 2  # Discomfort penalty

        # Temp Check
        if self.temp < CONFIG["limit_freeze"] or self.temp > CONFIG["limit_burn"]:
            self.alive = False
            penalty += 100
        elif (
            self.temp < CONFIG["ideal_temp_min"] or self.temp > CONFIG["ideal_temp_max"]
        ):
            penalty += 2

        self.total_penalty += penalty

    def get_fitness(self):
        # Formula: Reward for time alive - penalty for discomfort
        return (self.steps_survived**2) - self.total_penalty


# --- 3. THE EVOLUTION (Genetic Algorithm) ---
class GeneticAlgorithm:
    def __init__(self, population_size=50):
        self.pop_size = population_size
        self.population = [Brain() for _ in range(self.pop_size)]
        self.generation = 0
        self.best_fitness_history = []

    def evolve(self):
        # 1. Evaluate All Brains
        scores = []
        for brain in self.population:
            sim = SurvivalSimulation(brain)
            for _ in range(100):  # Max 100 steps
                if not sim.step():
                    break
            scores.append((sim.get_fitness(), brain))

        # Sort (Highest fitness first)
        scores.sort(key=lambda x: x[0], reverse=True)

        # Log Best Fitness
        best_fit = scores[0][0]
        self.best_fitness_history.append(best_fit)

        # 2. Create Next Generation
        new_pop = []

        # Elitism: Keep top 5
        for i in range(5):
            new_pop.append(scores[i][1])

        # Breeding (Crossover + Mutation)
        while len(new_pop) < self.pop_size:
            parent1 = self.tournament_select(scores)
            parent2 = self.tournament_select(scores)

            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_pop.append(child)

        self.population = new_pop
        self.generation += 1

        return best_fit, scores[0][1]  # Return best fitness & best brain

    def tournament_select(self, scores):
        # Pick 5 random, return the best
        candidates = [scores[np.random.randint(0, len(scores))] for _ in range(5)]
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def crossover(self, p1, p2):
        child = Brain()
        child.W1 = (p1.W1 + p2.W1) / 2
        child.W2 = (p1.W2 + p2.W2) / 2
        child.W3 = (p1.W3 + p2.W3) / 2
        return child

    def mutate(self, brain, rate=0.1):
        if np.random.rand() < rate:
            brain.W1 += np.random.randn(*brain.W1.shape) * 0.5
        if np.random.rand() < rate:
            brain.W3 += np.random.randn(*brain.W3.shape) * 0.5


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    ga = GeneticAlgorithm(population_size=50)
    best_brain = None

    print("--- EVOLUTION STARTED ---")
    for gen in range(100):
        fitness, brain = ga.evolve()
        best_brain = brain
        if gen % 10 == 0:
            print(f"Gen {gen}: Fitness Score = {fitness:.2f}")

    print("--- EVOLUTION COMPLETE ---")

    # --- FINAL VISUALIZATION ---
    # Run the best brain in a "Fixed Start" scenario for clear graph
    sim = SurvivalSimulation(best_brain, fixed_start=True)
    for _ in range(100):
        if not sim.step():
            break

    hist = sim.history

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # 1. Training Curve
    ax1.plot(ga.best_fitness_history, color="blue", linewidth=2)
    ax1.set_title("Evolutionary Progress (Fitness over Generations)")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness Score")
    ax1.grid(True)

    # 2. Gameplay
    steps = range(len(hist["food"]))
    ax2.plot(steps, hist["food"], label="Food", color="green", linewidth=2)
    ax2.plot(steps, hist["temp"], label="Temperature", color="red", linewidth=2)

    # Add Limits/Zones
    ax2.axhspan(
        CONFIG["ideal_temp_min"],
        CONFIG["ideal_temp_max"],
        color="orange",
        alpha=0.15,
        label="Comfort Temp",
    )
    ax2.axhspan(
        0, CONFIG["limit_starvation"], color="gray", alpha=0.2, label="Death Zone"
    )
    ax2.axhline(
        CONFIG["ideal_food_min"],
        color="green",
        linestyle="--",
        alpha=0.5,
        label="Target Food",
    )

    # Add Action Markers
    actions = np.array(hist["action"])
    ax2.scatter(
        np.where(actions == 1)[0],
        [hist["food"][i] for i in np.where(actions == 1)[0]],
        c="lime",
        marker="^",
        zorder=5,
        label="Eat",
    )
    ax2.scatter(
        np.where(actions == 2)[0],
        [hist["temp"][i] for i in np.where(actions == 2)[0]],
        c="darkred",
        marker="^",
        zorder=5,
        label="Heat",
    )
    ax2.scatter(
        np.where(actions == 3)[0],
        [hist["temp"][i] for i in np.where(actions == 3)[0]],
        c="blue",
        marker="v",
        zorder=5,
        label="Cool",
    )

    ax2.set_title("Best Agent Strategy")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
