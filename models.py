import math

def free_space(freq, max_km=10):
    distances = [d / 10 for d in range(1, int(max_km * 10))]
    losses = [
        32.44 + 20 * math.log10(freq) + 20 * math.log10(d)
        for d in distances
    ]
    return distances, losses

def hata(freq, hb, hm, max_km=10):
    distances = [d / 10 for d in range(1, int(max_km * 10))]
    losses = []
    for d in distances:
        a_hm = (1.1 * math.log10(freq) - 0.7) * hm - (1.56 * math.log10(freq) - 0.8)
        L = 69.55 + 26.16 * math.log10(freq) - 13.82 * math.log10(hb) - a_hm + \
            (44.9 - 6.55 * math.log10(hb)) * math.log10(d)
        losses.append(L)
    return distances, losses

def cost231_hata(freq, hb, hm, C, max_km=10):
    distances = [d / 10 for d in range(1, int(max_km * 10))]
    losses = []
    for d in distances:
        a_hm = (1.1 * math.log10(freq) - 0.7) * hm - (1.56 * math.log10(freq) - 0.8)
        L = 46.3 + 33.9 * math.log10(freq) - 13.82 * math.log10(hb) - a_hm + \
            (44.9 - 6.55 * math.log10(hb)) * math.log10(d) + C
        losses.append(L)
    return distances, losses

def itu_indoor(freq, n, max_m=100):
    distances = list(range(1, max_m))
    losses = [
        20 * math.log10(freq) + n * math.log10(d) + 28
        for d in distances
    ]
    return distances, losses

def log_distance(d0, d1, PL_d0, n, max_m=100):
    distances = list(range(1, max_m))
    losses = [
        PL_d0 + 10 * n * math.log10(d / d0)
        for d in distances
    ]
    return distances, losses

def okumura(freq, hb, hm, d_km, garea=10):
    distances = [d / 10 for d in range(10, int(d_km * 10))]  # 1 km to d_km
    losses = []

    for d in distances:
        # Free space loss
        lf = 32.45 + 20 * math.log10(freq) + 20 * math.log10(d)

        # Empirical corrections
        g_hb = 20 * math.log10(hb / 200)  # base station gain
        g_hm = 10 * math.log10(hm / 3)    # mobile station gain

        # Median attenuation (very simplified version)
        amu = 20 * math.log10(freq) + 10 * math.log10(d)

        L = lf + amu - g_hb - g_hm - garea
        losses.append(L)

    return distances, losses
