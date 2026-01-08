# config.py
# Bu dosya simülasyonun "Tanrı Modu" ayarlarıdır.

CONFIG = {
    # --- YSA AYARLARI ---
    "input_size": 3,  # Girdiler: Yiyecek, Sıcaklık, Konfor Farkı
    "hidden_size": 8,  # Beyin kapasitesi (Nöron sayısı)
    "output_size": 4,  # Çıktılar: Bekle, Ye, Isın, Serinle
    # --- BAŞLANGIÇ KOŞULLARI ---
    "max_food": 100,
    "start_food_min": 40,
    "start_food_max": 70,
    "start_temp_min": 15,
    "start_temp_max": 30,
    # --- ZORLUK AYARLARI (ENTROPİ) ---
    "decay_food": 3.0,  # Her turda ne kadar acıkıyor?
    "decay_temp": 1.0,  # Her turda hava ne kadar soğuyor?
    # --- AKSİYON GÜÇLERİ ---
    "action_eat_gain": 20.0,  # Yemek yiyince kaç puan artıyor?
    "action_heat_val": 5.0,  # Isınınca kaç derece artıyor?
    "action_cool_val": 5.0,  # Serinleyince kaç derece düşüyor?
    "action_energy_cost": 2.0,  # Isınmak/Serinlemek için harcanan yemek
    # --- YAŞAM SINIRLARI ---
    "limit_starvation": 10,  # Açlıktan ölme sınırı
    "limit_freeze": -10,  # Donarak ölme sınırı
    "limit_burn": 50,  # Yanarak ölme sınırı
    "ideal_temp_min": 20,  # İdeal sıcaklık alt sınırı
    "ideal_temp_max": 28,  # İdeal sıcaklık üst sınırı
    "ideal_food_min": 50,  # İdeal tokluk alt sınırı
}
