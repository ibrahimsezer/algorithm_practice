# utils.py
import numpy as np


def get_relative_info(agent_pos, target_pos, agent_angle):
    """
    Hedefin ajana göre nerede olduğunu hesaplar.
    Geriye 2 kritik bilgi döner:
    1. Mesafe: Hedef ne kadar uzakta? (0-1 arası normalize edilir)
    2. Açı Farkı: Hedef tam karşımda mı, sağımda mı, solumda mı?
    """
    dx = target_pos[0] - agent_pos[0]
    dy = target_pos[1] - agent_pos[1]

    # Hedefe olan kuş bakışı mesafe (Pisagor)
    distance = np.sqrt(dx**2 + dy**2)

    # Hedefin dünya üzerindeki açısı (Radyan)
    target_angle_global = np.arctan2(dy, dx)

    # Hedefin ajanın bakış yönüne göre açısı (Relative Angle)
    # Örn: Ajan 90 dereceye bakıyor, hedef 100 derecedeyse, fark +10 derecedir.
    angle_diff = target_angle_global - agent_angle

    # Açıyı -PI ile +PI arasına sıkıştır (Örn: 370 derece yerine 10 derece desin)
    angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi

    return distance, angle_diff
