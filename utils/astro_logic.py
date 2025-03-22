# utils/astro_logic.py

def detect_yogas(planet_positions, moon_pos, lagna_sign):
    yogas = []

    if "Jupiter" in planet_positions and "Moon" in planet_positions:
        jup = planet_positions["Jupiter"]
        moon = planet_positions["Moon"]
        if abs(jup["sign"] - moon["sign"]) in [4, 10]:
            yogas.append("Gajakesari Yoga")

    if "Mercury" in planet_positions and "Sun" in planet_positions:
        if planet_positions["Mercury"]["sign"] == planet_positions["Sun"]["sign"]:
            yogas.append("Budha-Aditya Yoga")

    if moon_pos["alone"]:
        yogas.append("Kemadruma Yoga")

    return yogas


def get_nakshatras(planet_longitudes, nakshatra_list):
    nakshatras = {}
    for planet, lon in planet_longitudes.items():
        index = int(lon / (360 / 27)) % 27
        nakshatras[planet] = nakshatra_list[index]
    return nakshatras


def get_remedies(yogas=[], dashas=[], nakshatras=[], language="en"):
    remedies = []

    if "Gajakesari Yoga" in yogas:
        remedies.append({
            "title": "Gajakesari Yoga",
            "remedy": {
                "en": "Worship Lord Ganesha on Wednesdays for wisdom.",
                "hi": "बुद्धवार को भगवान गणेश की पूजा करें।",
                "ta": "புதன்கிழமை விநாயகரைப் பூஜிக்கவும்.",
                "te": "బుధవారం వినాయకుని పూజించండి.",
                "ml": "ബുധനാഴ്ച വിനായകനെ പൂജിക്കുക.",
                "kn": "ಬುಧವಾರ ಗಣೇಶನ ಪೂಜೆ ಮಾಡಿರಿ."
            }
        })

    if "Kemadruma Yoga" in yogas:
        remedies.append({
            "title": "Kemadruma Yoga",
            "remedy": {
                "en": "Chant Moon beej mantra daily to reduce emotional fluctuations.",
                "hi": "चंद्र बीज मंत्र का रोज़ जाप करें।",
                "ta": "நிகழ்நிலை குறைக்க சந்திர பீஜ மந்திரம் ஜெபிக்கவும்.",
                "te": "చంద్ర బీజ మంత్రాన్ని జపించండి.",
                "ml": "ചന്ദ്ര ബീജ മന്ത്രം ജപിക്കുക.",
                "kn": "ಚಂದ್ರ ಬೀಜ ಮಂತ್ರ ಜಪಿಸಿ."
            }
        })

    return remedies
