from brain import Brain
from simulation_field import LunarLander
from genetic_algorithm import crossover, mutate
import numpy as np


# --- Puan Hesaplama Fonksiyonu ---
def puan_hesapla(sim):
    # Çakılırsa: Çarpma hızına göre ceza (0-50 puan)
    if sim.velocity < -2.0:
        impact = abs(sim.velocity)
        return max(0, 50 - impact)
    # İnerse: 100 puan + yakıt bonusu
    else:
        return 100 + sim.fuel


# --- EĞİTİM DÖNGÜSÜ ---
populasyon = [Brain() for _ in range(50)]  # 50 Pilot üret

print("--- EĞİTİM BAŞLIYOR ---")

for jenerasyon in range(50):  # 50 Nesil boyunca eğit
    scores = []

    # 1. Her pilotu test et
    for pilot in populasyon:
        sim = LunarLander()
        # Pilot maksimum 200 saniye uçabilir
        for _ in range(200):
            inputs = np.array([[sim.height / 100, sim.velocity / 20, sim.fuel / 100]])
            action = pilot.decide(inputs)
            durum = sim.step(action)
            if durum != "UCUYOR":
                break

        score = puan_hesapla(sim)
        scores.append((score, pilot))

    # 2. En iyileri seç (Puanı yüksek olanlar)
    scores.sort(key=lambda x: x[0], reverse=True)
    en_iyi_pilot = scores[0][1]
    en_iyi_puan = scores[0][0]

    if jenerasyon % 10 == 0:
        print(f"Jenerasyon {jenerasyon}: En İyi Puan = {en_iyi_puan:.1f}")

    # 3. Yeni nesil üret
    yeni_populasyon = []
    # En iyi 5 pilotu aynen aktar (Elitizm)
    for i in range(5):
        yeni_populasyon.append(scores[i][1])

    # Geri kalanları en iyilerden türet
    while len(yeni_populasyon) < 50:
        ebeveyn1 = scores[np.random.randint(0, 10)][1]
        ebeveyn2 = scores[np.random.randint(0, 10)][1]
        cocuk = crossover(ebeveyn1, ebeveyn2)
        mutate(cocuk)
        yeni_populasyon.append(cocuk)

    populasyon = yeni_populasyon

print("Eğitim Tamamlandı. En iyi pilot artık hazır.")
