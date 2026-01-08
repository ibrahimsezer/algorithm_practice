import numpy as np
from brain import Brain


def crossover(parent1, parent2):
    # Yeni bir beyin oluştur
    child = Brain()
    # Çocuğun genlerinin yarısı Anne'den, yarısı Baba'dan
    child.W1 = (parent1.W1 + parent2.W1) / 2
    child.W2 = (parent1.W2 + parent2.W2) / 2
    return child


def mutate(brain):
    # %10 ihtimalle beyindeki bir bağlantıyı rastgele değiştir
    if np.random.rand() < 0.1:
        brain.W1 += np.random.randn(*brain.W1.shape) * 0.5
    return brain


# --- MİNİ TEST 3: Çocuk Ebeveynlere Benziyor mu? ---
if __name__ == "__main__":
    anne = Brain()
    baba = Brain()

    # Annenin ilk ağırlığına bakalım
    print(f"Anne Geni (W1[0][0]): {anne.W1[0][0]:.4f}")
    print(f"Baba Geni (W1[0][0]): {baba.W1[0][0]:.4f}")

    cocuk = crossover(anne, baba)
    print(f"Çocuk Geni (Ortalaması olmalı): {cocuk.W1[0][0]:.4f}")
