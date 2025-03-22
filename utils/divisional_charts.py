import swisseph as swe
from datetime import datetime
from matplotlib import pyplot as plt
import os

def get_divisional_sign(degree, chart):
    if chart == "D9":  # Navamsa
        navamsa_size = 3.333333  # 30 / 9
        return int(degree // navamsa_size) + 1
    elif chart == "D10":  # Dasamsa
        dasamsa_size = 3.0  # 30 / 10
        return int(degree // dasamsa_size) + 1
    return 0

def calculate_divisional_chart(jd_ut, lat, lon, chart_type="D9"):
    swe.set_topo(lon, lat, 0)
    planets = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
               swe.VENUS, swe.SATURN, swe.TRUE_NODE]

    chart = {}
    for planet in planets:
        lon_deg, _ = swe.calc_ut(jd_ut, planet)
        sign = get_divisional_sign(lon_deg[0] % 30, chart_type)
        chart[swe.get_planet_name(planet)] = sign
    return chart

def plot_chart(chart_data, title, filename):
    plt.figure(figsize=(6, 6))
    plt.axis('off')
    plt.title(title, fontsize=14)

    # Draw 12 boxes in a square for Rasi format
    for i in range(12):
        x = (i % 4) * 1.5
        y = -(i // 4) * 1.5
        plt.gca().add_patch(plt.Rectangle((x, y), 1.5, 1.5, fill=None, edgecolor='black'))

    # Place planets inside boxes
    for planet, sign in chart_data.items():
        col = (sign - 1) % 4
        row = (sign - 1) // 4
        plt.text(col * 1.5 + 0.1, -row * 1.5 + 0.8, planet[:2], fontsize=9)

    out_path = f"static/{filename}"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    return out_path
