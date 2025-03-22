def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:  # Allow master numbers
        n = sum(map(int, str(n)))
    return n

def calculate_numerology(name: str, dob: str):
    import datetime
    name_value = sum([(ord(c.upper()) - 64) for c in name if c.isalpha()])

    # Life Path Number (from DOB)
    day, month, year = map(int, dob.split("-"))
    life_path = reduce_to_single_digit(day + month + year)

    # Destiny Number (from name)
    destiny = reduce_to_single_digit(name_value)

    # Soul Urge Number (vowels only)
    vowels = "AEIOU"
    soul_urge = reduce_to_single_digit(
        sum([(ord(c.upper()) - 64) for c in name if c.upper() in vowels])
    )

    # Personality Number (consonants only)
    consonants = [c for c in name if c.isalpha() and c.upper() not in vowels]
    personality = reduce_to_single_digit(
        sum([(ord(c.upper()) - 64) for c in consonants])
    )

    return {
        "name": name,
        "dob": dob,
        "lifePathNumber": life_path,
        "destinyNumber": destiny,
        "soulUrgeNumber": soul_urge,
        "personalityNumber": personality,
        "luckyNumbers": [life_path, destiny, (life_path + destiny) % 9 or 9],
    }
