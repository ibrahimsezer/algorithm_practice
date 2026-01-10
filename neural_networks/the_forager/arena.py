# arena.py
import numpy as np
from hunter import Hunter
from utils import get_relative_info


class Arena:
    def __init__(self):
        self.hunter = Hunter()
        self.target_pos = self.random_pos()
        self.width = 800
        self.height = 600

    def random_pos(self):
        return np.array(
            [
                np.random.rand() * 800 - 400,  # -400 ile +400 arası
                np.random.rand() * 600 - 300,
            ]
        )

    def reset(self):
        self.hunter = Hunter()  # Yeni bir avcı
        self.target_pos = self.random_pos()
        return self.hunter

    def step(self):
        # 1. Durumu Hesapla (Sensör)
        h_pos = np.array([self.hunter.x, self.hunter.y])
        dist, angle = get_relative_info(h_pos, self.target_pos, self.hunter.angle)

        # 2. Avcı Hamle Yapar
        self.hunter.think_and_move(dist, angle)

        # 3. Yeme Kontrolü (Hit Test)
        if dist < 20:  # 20 birim yaklaştıysa yemiş say
            self.hunter.score += 1
            self.hunter.energy += 50  # Ödül olarak enerji ver (Zaman kazanır)
            self.target_pos = self.random_pos()  # Yeni hedef oluştur
            return "YEDI"

        # 4. Sınır ve Enerji Kontrolü
        if self.hunter.energy <= 0:
            return "OLDU"  # Enerji bitti

        # Harita dışına çıkarsa ceza verip öldürebiliriz veya geri sektirebiliriz
        if abs(self.hunter.x) > self.width / 2 or abs(self.hunter.y) > self.height / 2:
            return "OLDU"  # Duvara çarptı

        return "DEVAM"
