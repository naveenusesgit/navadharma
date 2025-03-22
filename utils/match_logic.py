# utils/match_logic.py

from utils.astro_logic import get_dasha_info, calculate_astro_details

# Dummy nakshatra-guna mapping
GUNA_MAP = {
    'Ashwini': 'Deva', 'Bharani': 'Rakshasa', 'Krittika': 'Manushya',
    # ... fill for all 27 nakshatras
}

GUNA_SCORE = {
    ('Deva', 'Deva'): 6, ('Deva', 'Manushya'): 5, ('Deva', 'Rakshasa'): 1,
    ('Manushya', 'Manushya'): 6, ('Manushya', 'Rakshasa'): 3,
    ('Rakshasa', 'Rakshasa'): 6
}

def calculate_ashtakoot_score(nak1, nak2):
    guna1 = GUNA_MAP.get(nak1, 'Manushya')
    guna2 = GUNA_MAP.get(nak2, 'Manushya')
    return GUNA_SCORE.get((guna1, guna2), GUNA_SCORE.get((guna2, guna1), 0))

def check_dasha_compatibility(dasha1, dasha2):
    if dasha1['mahadasha'] == dasha2['mahadasha']:
        return "Both in same Mahadasha — similar life themes"
    if dasha1['antardasha'] == dasha2['antardasha']:
        return "Matching Antardasha — emotional synchronicity"
    return "Different Dashas — can indicate karmic balancing"

def match_compatibility(data1, data2):
    details1 = calculate_astro_details(data1)
    details2 = calculate_astro_details(data2)

    nak1 = details1.get('nakshatra', 'Ashwini')
    nak2 = details2.get('nakshatra', 'Ashwini')

    ashta_score = calculate_ashtakoot_score(nak1, nak2)
    dasha_msg = check_dasha_compatibility(details1.get('currentDasha', {}), details2.get('currentDasha', {}))

    return {
        "ashtakootScore": ashta_score,
        "ashtakootOutOf": 36,
        "dashaCompatibility": dasha_msg,
        "partner1": details1,
        "partner2": details2
    }
