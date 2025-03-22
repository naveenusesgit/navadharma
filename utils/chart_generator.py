import matplotlib.pyplot as plt
import os

def plot_chart(planet_positions, chart_title="Birth Chart", filename="birth_chart.png"):
    """
    Renders a basic circular chart of planet positions using matplotlib.
    Saves chart to 'static/' folder.
    """
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('E')
    ax.set_theta_direction(-1)
    ax.grid(True)

    ax.set_title(chart_title, va='bottom')

    # Plot each planet
    for planet, deg in planet_positions.items():
        rad = (360 - deg) * (3.14159 / 180.0)  # Convert degrees to radians clockwise
        ax.plot(rad, 1, 'o', label=planet)
        ax.text(rad, 1.05, planet, fontsize=10, ha='center')

    ax.set_rticks([])
    ax.set_yticklabels([])

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    output_path = os.path.join("static", filename)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    return output_path

def render_all_charts(planet_positions, divisional_charts: dict):
    """Renders multiple charts (D1, D9, D10, D7) and saves to PNGs"""
    os.makedirs("static", exist_ok=True)
    files = []

    files.append(plot_chart(planet_positions, "D1 - Birth Chart", "birth_chart.png"))

    for name, chart in divisional_charts.items():
        filename = f"{name.lower()}_chart.png"
        title = f"{name.upper()} - Divisional Chart"
        files.append(plot_chart(chart, title, filename))

    return files

