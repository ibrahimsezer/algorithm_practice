# hunter.py
import numpy as np
from brain import NeuralNetwork  # Senin eski brain.py dosyanı kullanıyoruz


class Hunter:
    def __init__(self):
        self.brain = NeuralNetwork(input_size=2, hidden_size=6, output_size=2)

        # Fiziksel Durum
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0  # Radyan cinsinden yönü (0 = Doğuya bakıyor)
        self.speed = 0.0

        # Skor
        self.score = 0
        self.energy = 100.0  # Enerji biterse oyun biter (Süre kısıtı)

    def think_and_move(self, target_dist, target_angle):
        # 1. Girdileri Hazırla
        # Mesafe 500 birimden fazlaysa 1.0 kabul et (Normalize)
        norm_dist = np.clip(target_dist / 500.0, 0, 1)
        # Açı farkını -1 ile 1 arasına sıkıştır
        norm_angle = target_angle / np.pi

        inputs = np.array([[norm_dist, norm_angle]])

        # 2. Beyne Sor
        outputs = self.brain.forward(inputs)

        # 3. Çıktıları Yorumla
        # Çıktı 0 (Turn): 0.5'ten küçükse Sola, büyükse Sağa dön
        # Çıktı 1 (Speed): Ne kadar hızlı gideyim?
        turn_force = (outputs[0][0] - 0.5) * 0.5  # Maksimum 0.25 radyan dön
        speed_force = outputs[0][1] * 5.0  # Maksimum 5 birim hız

        # 4. Hareketi Uygula
        self.angle += turn_force
        self.speed = speed_force

        self.x += np.cos(self.angle) * self.speed
        self.y += np.sin(self.angle) * self.speed

        # Enerji Tüketimi
        self.energy -= 0.5
