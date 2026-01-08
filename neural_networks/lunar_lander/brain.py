import numpy as np


class Brain:
    def __init__(self):
        # 3 Girdi: Yükseklik, Hız, Yakıt
        # 4 Gizli Nöron: Düşünme kapasitesi
        # 3 Çıktı: Motor Kapalı, %50 Güç, %100 Güç
        self.W1 = np.random.randn(3, 4)
        self.W2 = np.random.randn(4, 3)

    def decide(self, inputs):
        # 1. Katman (Düşünme)
        # Sigmoid: Sonuçları 0 ile 1 arasına sıkıştırır
        z1 = np.dot(inputs, self.W1)
        a1 = 1 / (1 + np.exp(-z1))

        # 2. Katman (Karar)
        z2 = np.dot(a1, self.W2)
        output = 1 / (1 + np.exp(-z2))

        # En yüksek değeri veren nöronun sırasını döndür (0, 1 veya 2)
        return np.argmax(output)


# --- MİNİ TEST 1: Beyin Çalışıyor mu? ---
if __name__ == "__main__":
    pilot = Brain()
    # Senaryo: Yükseklik 100m, Hız -50 m/s (Çakılıyor!), Yakıt %100
    sensor_verisi = np.array([[1.0, -1.0, 1.0]])
    karar = pilot.decide(sensor_verisi)

    print(f"Sensör Verisi: {sensor_verisi}")
    print(f"Pilotun Kararı: {karar}")
    print("(Not: Pilot henüz eğitilmediği için saçma bir karar verebilir, bu normal.)")
