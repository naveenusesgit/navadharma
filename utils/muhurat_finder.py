from utils.panchanga import get_panchanga
from utils.kundli import get_lagna_info
from datetime import datetime, timedelta

# Example marriage-friendly combos
GOOD_TITHIS = ['2', '3', '5', '7', '10', '11']
GOOD_NAKSHATRAS = ['Rohini', 'Uttara Phalguni', 'Hasta', 'Swati', 'Anuradha', 'Revati']
GOOD_YOGAS = ['Sukarman', 'Siddhi', 'Dhruva', 'Harshana']
GOOD_LAGNAS = ['Taurus', 'Libra', 'Cancer', 'Pisces']

def find_muhurats(date_str, latitude, longitude, timezone_offset):
    muhurats = []
    base_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    # Every 2 hours in the day (5 AM – 9 PM)
    for hour in range(5, 21, 2):
        dt = base_time.replace(hour=hour, minute=0, second=0)
        iso = dt.isoformat() + "Z"

        panchanga = get_panchanga(iso, latitude, longitude, timezone_offset)
        lagna = get_lagna_info(iso, latitude, longitude, timezone_offset)["lagna"]

        tithi_num = panchanga["tithi"].split()[1]
        nak = panchanga["nakshatra"].split("–")[0]
        yoga = panchanga["yoga"]

        # Simple scoring rule
        score = 0
        if tithi_num in GOOD_TITHIS: score += 1
        if nak in GOOD_NAKSHATRAS: score += 1
        if yoga in GOOD_YOGAS: score += 1
        if lagna in GOOD_LAGNAS: score += 1

        if score >= 3:
            muhurats.append({
                "time": dt.strftime("%H:%M"),
                "lagna": lagna,
                "tithi": panchanga["tithi"],
                "nakshatra": panchanga["nakshatra"],
                "yoga": yoga,
                "score": score
            })

    return muhurats
