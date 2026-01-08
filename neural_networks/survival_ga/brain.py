# brain.py
import numpy as np
from config import CONFIG


class Brain:
    def __init__(self):
        # Rastgele ağırlıklarla doğan bir beyin
        self.W1 = np.random.randn(CONFIG["input_size"], CONFIG["hidden_size"])
        self.b1 = np.zeros((1, CONFIG["hidden_size"]))

        self.W2 = np.random.randn(CONFIG["hidden_size"], CONFIG["hidden_size"])
        self.b2 = np.zeros((1, CONFIG["hidden_size"]))

        self.W3 = np.random.randn(CONFIG["hidden_size"], CONFIG["output_size"])
        self.b3 = np.zeros((1, CONFIG["output_size"]))

    def sigmoid(self, x):
        # Aktivasyon fonksiyonu (Sonuçları 0-1 arasına sıkıştırır)
        return 1 / (1 + np.exp(-x))

    def decide(self, inputs):
        """
        Sensör verilerini al -> Düşün -> En mantıklı aksiyonu seç
        inputs: [Food_Normalized, Temp_Normalized, Temp_Difference]
        """
        # Katman 1
        z1 = np.dot(inputs, self.W1) + self.b1
        a1 = self.sigmoid(z1)

        # Katman 2 (Derin Düşünce)
        z2 = np.dot(a1, self.W2) + self.b2
        a2 = self.sigmoid(z2)

        # Çıktı Katmanı (Karar Anı)
        z3 = np.dot(a2, self.W3) + self.b3
        output = self.sigmoid(z3)

        # En yüksek puanı alan nöronun sırasını döndür (0, 1, 2 veya 3)
        return np.argmax(output)


# --- MİNİ TEST ---
if __name__ == "__main__":
    test_brain = Brain()
    # Örnek Durum: Yemek az (0.2), Sıcaklık İdeal (0.5), Fark Yok (0.0)
    ornek_veri = np.array([[0.2, 0.5, 0.0]])
    karar = test_brain.decide(ornek_veri)
    print(f"Rastgele Beynin Kararı: {karar} (0:Bekle, 1:Ye, 2:Isın, 3:Serinle)")
