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

def calculate_dasha_periods(dob, starting_dasha):
    periods = []
    current_dasha = starting_dasha
    start_date = dob
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

def get_current_dasha_periods(jd, dob):
    swe.set_ephe_path('.')
    moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
    starting_dasha = get_starting_dasha(moon_pos)
    dasha_periods = calculate_dasha_periods(dob, starting_dasha)

    today = datetime.utcnow().date()
    for period in dasha_periods:
        start = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start <= today <= end:
            return {
                "current_dasha": period['dasha'],
                "start_date": period['start'],
                "end_date": period['end']
            }
    return {"current_dasha": "Unknown"}
