from datetime import datetime
from utils.astro_utils import get_planet_positions_for_datetime
from utils.gpt_summary import gpt_summary

def get_today_transits():
    now = datetime.utcnow()
    return get_planet_positions_for_datetime(now)

async def get_gpt_transit_summary(transits: dict):
    planet_lines = [f"{planet} is in {info['sign']} at {info['degree']:.2f}°" for planet, info in transits.items()]
    prompt = (
        "Provide a daily astrological summary based on these planetary positions:\n"
        + "\n".join(planet_lines)
    )
    return await gpt_summary(prompt)
