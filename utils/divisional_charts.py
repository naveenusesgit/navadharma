import swisseph as swe
import matplotlib.pyplot as plt
import os
from datetime import datetime

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
CHART_STYLES = ["south", "north"]

DIVISIONAL_FACTORS = {
    "D1": 1,
    "D3": 3,
    "D7": 7,
    "D9": 9,
    "D10": 10,
    "D12": 12,
    "D24": 24,
    "D60": 60
}


def get_divisional_sign(degree, factor):
    division = 360 / (12 * factor)
    division_index = int(degree / division)
    return division_index % 12


def calculate_divisional_chart(jd, lat, lon, chart_type="D9"):
    swe.set_topo(lon, lat, 0)
    chart = {i: [] for i in range(12)}

    factor = DIVISIONAL_FACTORS.get(chart_type.upper(), 9)

    for planet in PLANETS:
        planet_id = getattr(swe, planet.upper())
        lon, _ = swe.calc_ut(jd, planet_id)
        sign = get_divisional_sign(lon, factor)
        chart[sign].append(planet)

    return chart


def draw_south_chart(chart, title="Chart", filename="chart.png"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.axis('off')

    grid_pos = [
        (0, 2), (0, 1), (0, 0),
        (1, 0), (2, 0), (2, 1),
        (2, 2), (2, 3), (1, 3),
        (0, 3), (1, 2), (1, 1)
    ]

    for i, pos in enumerate(grid_pos):
        x, y = pos
        rect = plt.Rectangle((x, y), 1, 1, fill=False)
        ax.add_patch(rect)
        planets = ','.join(chart.get(i, []))
        ax.text(x + 0.5, y + 0.5, f"{i+1}\n{planets}", ha='center', va='center', fontsize=8)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    path = f"static/{filename}"
    plt.savefig(path)
    plt.close()
    return path


def draw_north_chart(chart, title="Chart", filename="chart.png"):
    # Placeholder for North Indian style rendering
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(f"{title} (North Style)")
    ax.axis('off')

    for i in range(12):
        angle = i * 30
        x = 2 + 1.5 * (i % 4)
        y = 2 + 1.5 * (i // 4)
        planets = ','.join(chart.get(i, []))
        ax.text(x, y, f"{i+1}\n{planets}", ha='center', va='center', fontsize=8)

    path = f"static/{filename}"
    plt.savefig(path)
    plt.close()
    return path


def plot_chart(chart, title, filename, style="south"):
    os.makedirs("static", exist_ok=True)
    if style == "north":
        return draw_north_chart(chart, title, filename)
    else:
        return draw_south_chart(chart, title, filename)
