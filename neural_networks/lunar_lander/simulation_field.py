class LunarLander:
    def __init__(self):
        self.height = 100.0  # 100 metreden başlıyoruz
        self.velocity = 0.0  # Hızımız başta 0
        self.fuel = 100.0  # Depo dolu
        self.gravity = -0.5  # Yerçekimi aşağı çeker
        self.alive = True  # Hala havada mı?

    def step(self, action):
        """
        action: 0 (Bekle), 1 (Hafif Gaz), 2 (Tam Gaz)
        """
        if not self.alive:
            return

        thrust = 0.0

        # Motor Mantığı
        if self.fuel > 0:
            if action == 1:
                thrust = 0.8
                self.fuel -= 1.5
            elif action == 2:
                thrust = 1.5
                self.fuel -= 3.0

        # Fizik Hesaplaması (F = m*a mantığının basiti)
        acceleration = self.gravity + thrust
        self.velocity += acceleration
        self.height += self.velocity

        # Yere Çarpma Kontrolü
        if self.height <= 0:
            self.height = 0
            self.alive = False
            # Hız -2.0'dan büyükse (örn -0.5) yumuşak inmiştir
            if self.velocity >= -2.0:
                return "BASARILI_INIS"
            else:
                return "CAKILDI"

        return "UCUYOR"


# --- MİNİ TEST 2: Fizik Çalışıyor mu? ---
if __name__ == "__main__":
    arac = LunarLander()
    print("Simülasyon Başladı! (Motoru hiç çalıştırmazsak ne olur?)")

    for t in range(15):  # 15 saniye izleyelim
        durum = arac.step(action=0)  # 0 = Motor Kapalı
        print(f"Saniye {t}: Yükseklik={arac.height:.1f}m, Hız={arac.velocity:.1f}m/s")

        if durum != "UCUYOR":
            print(f"SONUÇ: {durum}")
            break
