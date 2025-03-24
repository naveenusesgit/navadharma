import swisseph as swe
from datetime import datetime, timedelta

DASHA_SEQUENCE = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
    'Rahu', 'Jupiter', 'Saturn', 'Mercury'
]

DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
    'Mars': 7, 'Rahu': 18, 'Jupiter': 16,
    'Saturn': 19, 'Mercury': 17
}

def get_starting_dasha(moon_longitude):
    segment = int((moon_longitude % 120) // (120 / 9))
    return DASHA_SEQUENCE[segment]

def calculate_dasha_periods(start_date, starting_dasha):
    periods = []
    current_dasha = starting_dasha
    for _ in range(len(DASHA_SEQUENCE)):
        duration_years = DASHA_YEARS[current_dasha]
        end_date = start_date + timedelta(days=duration_years * 365.25)
        periods.append({
            'dasha': current_dasha,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        })
        start_date = end_date
        current_index = DASHA_SEQUENCE.index(current_dasha)
        current_dasha = DASHA_SEQUENCE[(current_index + 1) % len(DASHA_SEQUENCE)]
    return periods

def calculate_antar_dasha_periods(mahadasha, start_date):
    total_years = DASHA_YEARS[mahadasha]
    antar_dashas = []
    current_start = start_date

    for sub_dasha in DASHA_SEQUENCE:
        weight = DASHA_YEARS[sub_dasha] / 120
        duration_days = total_years * weight * 365.25
        current_end = current_start + timedelta(days=duration_days)
        antar_dashas.append({
            'antar_dasha': sub_dasha,
            'start': current_start.strftime('%Y-%m-%d'),
            'end': current_end.strftime('%Y-%m-%d')
        })
        current_start = current_end

    return antar_dashas

def get_current_dasha_periods(jd, dob):
    swe.set_ephe_path('.')
    moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
    starting_dasha = get_starting_dasha(moon_pos)
    mahadasha_periods = calculate_dasha_periods(dob, starting_dasha)

    today = datetime.utcnow().date()
    current_mahadasha = None
    current_antar_dasha = None

    for period in mahadasha_periods:
        start = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start <= today <= end:
            current_mahadasha = period
            antar_dashas = calculate_antar_dasha_periods(period['dasha'], start)
            for antar in antar_dashas:
                antar_start = datetime.strptime(antar['start'], '%Y-%m-%d').date()
                antar_end = datetime.strptime(antar['end'], '%Y-%m-%d').date()
                if antar_start <= today <= antar_end:
                    current_antar_dasha = antar
                    break
            break

    return {
        "mahadasha": current_mahadasha,
        "antar_dasha": current_antar_dasha
    }
