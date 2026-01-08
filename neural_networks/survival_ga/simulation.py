# simulation.py
import numpy as np
from config import CONFIG


class SurvivalSimulation:
    def __init__(self, brain, fixed_start=False):
        self.brain = brain
        self.alive = True
        self.steps_survived = 0
        self.total_penalty = 0

        # Grafik çizmek için geçmişi kaydediyoruz
        self.history = {"food": [], "temp": [], "action": []}

        # Başlangıç Durumu
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
        # Verileri normalize et (0.0 ile 1.0 arasına çek)
        # Yapay zeka küçük sayılarla daha iyi çalışır.
        norm_food = self.food / CONFIG["max_food"]
        norm_temp = self.temp / 50.0  # 50 dereceyi baz alıyoruz

        # Kritik Bilgi: İdealden ne kadar uzağım?
        ideal_center = (CONFIG["ideal_temp_max"] + CONFIG["ideal_temp_min"]) / 2
        temp_diff = (self.temp - ideal_center) / 24.0

        return np.array([[norm_food, norm_temp, temp_diff]])

    def step(self):
        if not self.alive:
            return False

        # 1. Beyne sor
        inputs = self.get_inputs()
        action = self.brain.decide(inputs)

        # Kayıt tut
        self.history["food"].append(self.food)
        self.history["temp"].append(self.temp)
        self.history["action"].append(action)

        # 2. Doğal Tüketim (Entropi)
        self.food -= CONFIG["decay_food"]
        self.temp -= CONFIG["decay_temp"]

        # 3. Aksiyonu Uygula
        if action == 1:  # Ye
            self.food += CONFIG["action_eat_gain"]
        elif action == 2:  # Isın
            self.temp += CONFIG["action_heat_val"]
            self.food -= CONFIG["action_energy_cost"]  # Isınmak enerji harcatır
        elif action == 3:  # Serinle
            self.temp -= CONFIG["action_cool_val"]
            self.food -= CONFIG["action_energy_cost"]  # Serinlemek enerji harcatır

        # Sınırları koru (Yiyecek 100'ü geçemez vb.)
        self.food = np.clip(self.food, 0, CONFIG["max_food"])
        self.temp = np.clip(self.temp, -20, 60)

        # 4. Yaşam Kontrolü
        self.check_vital_signs()

        self.steps_survived += 1
        return self.alive

    def check_vital_signs(self):
        penalty = 0

        # Açlık Kontrolü
        if self.food < CONFIG["limit_starvation"]:
            self.alive = False
            penalty += 50
        elif self.food < CONFIG["ideal_food_min"]:
            penalty += 1  # Rahatsızlık cezası

        # Sıcaklık Kontrolü
        if self.temp < CONFIG["limit_freeze"] or self.temp > CONFIG["limit_burn"]:
            self.alive = False
            penalty += 50
        elif (
            self.temp < CONFIG["ideal_temp_min"] or self.temp > CONFIG["ideal_temp_max"]
        ):
            penalty += 1  # Konforsuzluk cezası

        self.total_penalty += penalty

    def get_fitness(self):
        # Amaç: Uzun süre yaşamak (steps^2) ve az acı çekmek (-penalty)
        return (self.steps_survived**2) - self.total_penalty
