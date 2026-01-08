import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
CONFIG = {
    "start_height": 100.0,
    "start_fuel": 100.0,
    "gravity": -0.5,  # Her adımda hızı aşağı çeken kuvvet
    "thrust_soft": 0.8,  # Yerçekimini yenen hafif güç
    "thrust_hard": 1.5,  # Yerçekimini yenen güçlü güç
    "fuel_cost_soft": 1.5,
    "fuel_cost_hard": 3.0,
    "safe_landing_speed": -2.0,  # Bu hızdan yavaşsa (örn -1.0) başarılı
    "max_speed_terminal": -20.0,  # Maksimum düşüş hızı (normalize için)
}


# --- 1. THE BRAIN (Aynen Koruyoruz) ---
class Brain:
    def __init__(self):
        # Input: Height, Velocity, Fuel
        self.W1 = np.random.randn(3, 8)
        self.b1 = np.zeros((1, 8))
        self.W2 = np.random.randn(8, 8)
        self.b2 = np.zeros((1, 8))
        self.W3 = np.random.randn(8, 3)  # Output: 0, 1, 2 (Actions)
        self.b3 = np.zeros((1, 3))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def decide(self, inputs):
        z1 = np.dot(inputs, self.W1) + self.b1
        a1 = self.sigmoid(z1)
        z2 = np.dot(a1, self.W2) + self.b2
        a2 = self.sigmoid(z2)
        z3 = np.dot(a2, self.W3) + self.b3
        output = self.sigmoid(z3)
        return np.argmax(output)


# --- 2. PHYSICS ENGINE (Lunar Lander Simulation) ---
class LanderSimulation:
    def __init__(self, brain):
        self.brain = brain
        self.height = CONFIG["start_height"]
        self.velocity = 0.0  # Başlangıçta duruyor, sonra düşecek
        self.fuel = CONFIG["start_fuel"]

        self.landed = False
        self.crashed = False
        self.history = {"height": [], "velocity": [], "thrust": []}

    def get_inputs(self):
        # Normalization is crucial for Neural Networks
        norm_height = self.height / CONFIG["start_height"]
        # Velocity is usually negative (falling), map -20..0 to -1..0
        norm_velocity = self.velocity / abs(CONFIG["max_speed_terminal"])
        norm_fuel = self.fuel / CONFIG["start_fuel"]

        return np.array([[norm_height, norm_velocity, norm_fuel]])

    def step(self):
        if self.landed or self.crashed:
            return False

        # 1. AI Decides
        inputs = self.get_inputs()
        action = self.brain.decide(inputs)

        thrust_val = 0.0

        # 2. Physics & Fuel Logic
        if self.fuel > 0:
            if action == 1:  # Soft Thrust
                thrust_val = CONFIG["thrust_soft"]
                self.fuel -= CONFIG["fuel_cost_soft"]
            elif action == 2:  # Hard Thrust
                thrust_val = CONFIG["thrust_hard"]
                self.fuel -= CONFIG["fuel_cost_hard"]

        # 3. Update Physics (Velocity & Position)
        # Acceleration = Gravity + Thrust
        acceleration = CONFIG["gravity"] + thrust_val
        self.velocity += acceleration
        self.height += self.velocity

        # 4. Record History
        self.history["height"].append(self.height)
        self.history["velocity"].append(self.velocity)
        self.history["thrust"].append(thrust_val)

        # 5. Check Ground Collision
        if self.height <= 0:
            self.height = 0
            if self.velocity >= CONFIG["safe_landing_speed"]:
                self.landed = True  # SUCCESS
            else:
                self.crashed = True  # FAIL
            return False  # Simulation ends

        return True  # Continue

    def get_fitness(self):
        # Fitness Logic:
        # 1. Did it crash? Huge penalty based on impact speed.
        # 2. Did it land? Reward based on how soft the landing was.
        # 3. Fuel Bonus: Efficiency is good but secondary.

        if self.crashed:
            # Impact speed is negative (e.g., -15). The faster it crashes, lower the score.
            # Score range: 0 to 50
            impact_severity = abs(self.velocity)
            return max(0, 50 - impact_severity * 2)

        elif self.landed:
            # Successful landing! Base score 100.
            # Bonus for very soft landing (velocity close to 0)
            softness_bonus = (CONFIG["safe_landing_speed"] - self.velocity) * 20
            fuel_bonus = self.fuel * 0.5
            return 100 + softness_bonus + fuel_bonus

        else:
            # Still flying (should not happen if loop limits are set correctly)
            return 0


# --- 3. GENETIC ALGORITHM ---
class GeneticPilot:
    def __init__(self, pop_size=50):
        self.pop_size = pop_size
        self.population = [Brain() for _ in range(pop_size)]
        self.best_scores = []

    def evolve(self, generations=50):
        print("--- MISSION CONTROL: TRAINING STARTED ---")

        for gen in range(generations):
            scores = []

            for brain in self.population:
                sim = LanderSimulation(brain)
                # Max 200 steps to land
                for _ in range(200):
                    if not sim.step():
                        break
                scores.append((sim.get_fitness(), brain))

            # Sort descending
            scores.sort(key=lambda x: x[0], reverse=True)
            best_score = scores[0][0]
            self.best_scores.append(best_score)

            if gen % 10 == 0:
                print(f"Gen {gen}: Best Score = {best_score:.1f}")

            # Selection & Crossover
            new_pop = [scores[i][1] for i in range(5)]  # Keep top 5 elites

            while len(new_pop) < self.pop_size:
                # Simple Tournament
                p1 = scores[np.random.randint(0, 15)][1]
                p2 = scores[np.random.randint(0, 15)][1]
                child = self.crossover(p1, p2)
                self.mutate(child)
                new_pop.append(child)

            self.population = new_pop

        return scores[0][1]  # Return best brain

    def crossover(self, p1, p2):
        child = Brain()
        child.W1 = (p1.W1 + p2.W1) / 2
        child.W2 = (p1.W2 + p2.W2) / 2
        child.W3 = (p1.W3 + p2.W3) / 2
        return child

    def mutate(self, brain):
        if np.random.rand() < 0.1:
            brain.W1 += np.random.randn(*brain.W1.shape) * 0.5
        if np.random.rand() < 0.1:
            brain.W3 += np.random.randn(*brain.W3.shape) * 0.5


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    pilot_school = GeneticPilot(pop_size=50)
    best_pilot = pilot_school.evolve(generations=80)

    # --- VISUALIZATION ---
    sim = LanderSimulation(best_pilot)
    for _ in range(300):
        if not sim.step():
            break

    hist = sim.history
    time_steps = range(len(hist["height"]))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # Plot 1: Height & Velocity
    ax1.plot(time_steps, hist["height"], label="Altitude (m)", color="blue")
    ax1.axhline(0, color="black", linewidth=2, label="Ground")

    # Create a twin axis to show velocity on the same graph
    ax1_twin = ax1.twinx()
    ax1_twin.plot(
        time_steps,
        hist["velocity"],
        label="Velocity (m/s)",
        color="red",
        linestyle="--",
    )
    ax1_twin.axhline(
        CONFIG["safe_landing_speed"],
        color="green",
        linestyle=":",
        label="Safe Speed Limit",
    )

    ax1.set_title(
        f"Landing Telemetry (Status: {'LANDED' if sim.landed else 'CRASHED'})"
    )
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Height")
    ax1_twin.set_ylabel("Velocity")
    ax1.legend(loc="upper left")
    ax1_twin.legend(loc="upper right")
    ax1.grid(True)

    # Plot 2: Thruster Usage
    ax2.plot(
        time_steps,
        hist["thrust"],
        color="orange",
        drawstyle="steps-post",
        fillstyle="full",
    )
    ax2.fill_between(time_steps, hist["thrust"], step="post", alpha=0.4, color="orange")
    ax2.set_title("Thruster Engine Output")
    ax2.set_ylabel("Thrust Power")
    ax2.set_xlabel("Time")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
