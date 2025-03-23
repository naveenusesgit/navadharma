from datetime import datetime, timedelta

# Vimshottari Dasha configuration
PLANETS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = {
    'Ketu': 7,
    'Venus': 20,
    'Sun': 6,
    'Moon': 10,
    'Mars': 7,
    'Rahu': 18,
    'Jupiter': 16,
    'Saturn': 19,
    'Mercury': 17
}

# Get Vimshottari Dasha sequence starting from the current nakshatra lord
def get_dasha_sequence(start_index, start_date, total_period=120):
    sequence = []
    date = start_date

    for i in range(len(PLANETS)):
        idx = (start_index + i) % len(PLANETS)
        planet = PLANETS[idx]
        years = DASHA_YEARS[planet]
        duration_days = int(years * 365.25)
        end_date = date + timedelta(days=duration_days)

        sequence.append({
            "maha_dasha": planet,
            "start": date.strftime('%Y-%m-%d'),
            "end": end_date.strftime('%Y-%m-%d')
        })

        date = end_date
        if (date - start_date).days > total_period * 365:
            break

    return sequence

# Calculate Antar Dasha (sub-periods) within a Mahadasha
def get_antar_dashas(mahadasha_lord, start_date):
    antar_dashas = []
    total_days = int(DASHA_YEARS[mahadasha_lord] * 365.25)
    date = start_date

    for sub_lord in PLANETS:
        proportion = DASHA_YEARS[sub_lord] / 120  # Vimshottari total cycle = 120 years
        duration = int(proportion * total_days)
        end_date = date + timedelta(days=duration)
        antar_dashas.append({
            "antar_dasha": sub_lord,
            "start": date.strftime('%Y-%m-%d'),
            "end": end_date.strftime('%Y-%m-%d')
        })
        date = end_date

    return antar_dashas

# Determine current Dasha (Mahadasha + Antar Dasha) from Nakshatra and time
def get_current_dasha(julian_day, moon_longitude, base_date=None):
    if base_date is None:
        base_date = datetime.utcnow()

    # Determine the Nakshatra index
    nakshatra_index = int(moon_longitude / 13.3333)  # 13°20' per nakshatra
    nakshatra_lord_index = nakshatra_index % len(PLANETS)

    dasha_sequence = get_dasha_sequence(nakshatra_lord_index, base_date)

    now = datetime.utcnow()
    current_dasha = None

    for maha in dasha_sequence:
        start = datetime.strptime(maha['start'], '%Y-%m-%d')
        end = datetime.strptime(maha['end'], '%Y-%m-%d')
        if start <= now <= end:
            antar_dashas = get_antar_dashas(maha['maha_dasha'], start)
            for antar in antar_dashas:
                antar_start = datetime.strptime(antar['start'], '%Y-%m-%d')
                antar_end = datetime.strptime(antar['end'], '%Y-%m-%d')
                if antar_start <= now <= antar_end:
                    current_dasha = {
                        "current_maha_dasha": maha['maha_dasha'],
                        "maha_dasha_ends": maha['end'],
                        "current_antar_dasha": antar['antar_dasha'],
                        "antar_dasha_ends": antar['end'],
                        "next_maha_dashas": dasha_sequence[:3],
                        "next_antar_dashas": antar_dashas[:3]
                    }
                    break
            break

    return current_dasha
