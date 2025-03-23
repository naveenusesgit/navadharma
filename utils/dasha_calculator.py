from datetime import datetime, timedelta
import swisseph as swe

# Dasha Lords & Years
DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
    ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

def get_current_dasha(jd, moon_long):
    # Nakshatra calculation
    total_nakshatra_deg = 13 + 1/3  # 13°20'
    nak_index = int(moon_long // total_nakshatra_deg)
    nak_deg = moon_long % total_nakshatra_deg

    # Get Dasha lord
    dasha_lord_index = nak_index % 9
    dasha_lord, dasha_years = DASHA_SEQUENCE[dasha_lord_index]

    # Calculate balance of first Maha Dasha based on position in nakshatra
    percentage_completed = nak_deg / total_nakshatra_deg
    balance_years = (1 - percentage_completed) * dasha_years
    balance_days = int(balance_years * 365.25)

    # Start date of first Dasha
    birth_date = swe.revjul(jd)  # returns tuple (year, month, day, ...)
    birth_dt = datetime(birth_date[0], birth_date[1], birth_date[2])

    dasha_start = birth_dt
    dasha_end = dasha_start + timedelta(days=balance_days)

    # Maha Dasha cycle (next 3 dashas for preview)
    dasha_cycle = []
    index = dasha_lord_index
    current_date = dasha_start

    for _ in range(3):
        lord, years = DASHA_SEQUENCE[index % len(DASHA_SEQUENCE)]
        start = current_date
        end = start + timedelta(days=int(years * 365.25))
        dasha_cycle.append({
            "maha_dasha": lord,
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        })
        current_date = end
        index += 1

    return {
        "current_maha_dasha": dasha_lord,
        "maha_dasha_ends": dasha_end.strftime("%Y-%m-%d"),
        "dasha_preview": dasha_cycle
    }
