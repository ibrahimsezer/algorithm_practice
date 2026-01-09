# main.py
import numpy as np
import matplotlib.pyplot as plt
from config import CONFIG
from brain import Brain
from simulation import SurvivalSimulation


class GeneticAlgorithm:
    def __init__(self, population_size=50):
        self.pop_size = population_size
        self.population = [Brain() for _ in range(self.pop_size)]
        self.history_best_fitness = []

    def crossover(self, p1, p2):
        child = Brain()
        # Genlerin karışımı (Ortalama Alma Yöntemi)
        child.W1 = (p1.W1 + p2.W1) / 2
        child.W2 = (p1.W2 + p2.W2) / 2
        child.W3 = (p1.W3 + p2.W3) / 2
        return child

    def mutate(self, brain, rate=0.1):
        # Rastgele mutasyon (Evrimsel sıçrama)
        if np.random.rand() < rate:
            brain.W1 += np.random.randn(*brain.W1.shape) * 0.5
        if np.random.rand() < rate:
            brain.W3 += np.random.randn(*brain.W3.shape) * 0.5

    def evolve(self, generations=50):
        print(f"--- EVRİM BAŞLIYOR ({generations} Nesil) ---")

        for gen in range(generations):
            scores = []

            # Her bireyi test et
            for brain in self.population:
                sim = SurvivalSimulation(brain)
                for _ in range(100):  # Maksimum 100 adım yaşayabilir
                    if not sim.step():
                        break
                scores.append((sim.get_fitness(), brain))

            # En iyiden en kötüye sırala
            scores.sort(key=lambda x: x[0], reverse=True)
            best_fit = scores[0][0]
            self.history_best_fitness.append(best_fit)

            if gen % 10 == 0:
                print(f"Nesil {gen}: En İyi Puan = {best_fit:.1f}")

            # Yeni Nesil Oluşturma
            new_pop = []

            # Elitizm: En iyi 5 bireyi aynen koru
            for i in range(5):
                new_pop.append(scores[i][1])

            # Geri kalanları üret
            while len(new_pop) < self.pop_size:
                # Turnuva Seçimi (Rastgele 5 kişiden en iyisi ebeveyn olur)
                candidates = [
                    scores[np.random.randint(0, len(scores))] for _ in range(5)
                ]
                candidates.sort(key=lambda x: x[0], reverse=True)
                parent1 = candidates[0][1]

                candidates2 = [
                    scores[np.random.randint(0, len(scores))] for _ in range(5)
                ]
                candidates2.sort(key=lambda x: x[0], reverse=True)
                parent2 = candidates2[0][1]

                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_pop.append(child)

            self.population = new_pop

        return scores[0][1]  # En iyi beyni döndür


# --- ÇALIŞTIRMA VE GRAFİK ---
if __name__ == "__main__":
    ga = GeneticAlgorithm(population_size=50)
    best_brain = ga.evolve(generations=100)

    # En iyi ajanı izlemek için son bir test yap (Sabit başlangıç ile)
    print("\n--- SONUÇ SİMÜLASYONU BAŞLATILIYOR ---")
    sim = SurvivalSimulation(best_brain, fixed_start=True)
    for _ in range(100):
        if not sim.step():
            break

    # --- GRAFİK ÇİZİMİ ---
    hist = sim.history
    steps = range(len(hist["food"]))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Grafik 1: Öğrenme Eğrisi
    ax1.plot(ga.history_best_fitness, color="blue", linewidth=2)
    ax1.set_title("Evrimsel Gelişim (Puan)")
    ax1.set_xlabel("Nesil")
    ax1.set_ylabel("Fitness Skoru")
    ax1.grid(True, alpha=0.3)

    # Grafik 2: Ajanın Stratejisi
    ax2.plot(steps, hist["food"], label="Yiyecek", color="green", linewidth=2)
    ax2.plot(steps, hist["temp"], label="Sıcaklık", color="red", linewidth=2)

    # Bölgeleri Boya
    ax2.axhspan(
        CONFIG["ideal_temp_min"],
        CONFIG["ideal_temp_max"],
        color="orange",
        alpha=0.15,
        label="İdeal Isı",
    )
    ax2.axhspan(
        0, CONFIG["limit_starvation"], color="gray", alpha=0.2, label="Ölüm Bölgesi"
    )
    ax2.axhline(
        CONFIG["ideal_food_min"],
        color="green",
        linestyle="--",
        alpha=0.5,
        label="Hedef Tokluk",
    )

    # Aksiyonları İşaretle (Üçgenler)
    actions = np.array(hist["action"])

    # Ne zaman yedi? (Yeşil Üçgen)
    eat_idx = np.where(actions == 1)[0]
    ax2.scatter(
        eat_idx,
        [hist["food"][i] for i in eat_idx],
        c="lime",
        marker="^",
        zorder=5,
        s=50,
        label="Eylem: Ye",
    )

    # Ne zaman ısındı? (Kırmızı Üçgen)
    heat_idx = np.where(actions == 2)[0]
    ax2.scatter(
        heat_idx,
        [hist["temp"][i] for i in heat_idx],
        c="darkred",
        marker="^",
        zorder=5,
        s=50,
        label="Eylem: Isın",
    )

    # Ne zaman serinledi? (Mavi Ters Üçgen)
    cool_idx = np.where(actions == 3)[0]
    ax2.scatter(
        cool_idx,
        [hist["temp"][i] for i in cool_idx],
        c="blue",
        marker="v",
        zorder=5,
        s=50,
        label="Eylem: Serinle",
    )

    ax2.set_title(f"En İyi Ajanın Hayatta Kalma Stratejisi ({len(steps)} Adım Yaşadı)")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
