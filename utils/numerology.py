# utils/numerology.py

from datetime import datetime
import re

VOWELS = "AEIOU"

def reduce_to_digit(n):
    """Reduces a number to a single digit or master number (11, 22, 33)."""
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_life_path_number(dob: str) -> int:
    """Calculate the Life Path Number from date of birth."""
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        total = (
            sum(int(d) for d in str(birth_date.year)) +
            sum(int(d) for d in str(birth_date.month)) +
            sum(int(d) for d in str(birth_date.day))
        )
        return reduce_to_digit(total)
    except Exception as e:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.") from e

def letter_to_number(letter):
    """Map letters to numbers per numerology chart."""
    mapping = {
        1: "AJS",
        2: "BKT",
        3: "CLU",
        4: "DMV",
        5: "ENW",
        6: "FOX",
        7: "GPY",
        8: "HQZ",
        9: "IR"
    }
    for number, letters in mapping.items():
        if letter.upper() in letters:
            return number
    return 0

def calculate_destiny_number(name: str) -> int:
    """Calculate Destiny Number (Expression Number) from full name."""
    clean_name = re.sub(r"[^A-Z]", "", name.upper())
    total = sum(letter_to_number(char) for char in clean_name)
    return reduce_to_digit(total)

def calculate_soul_urge_number(name: str) -> int:
    """Calculate Soul Urge Number from vowels in the name."""
    clean_name = re.sub(r"[^A-Z]", "", name.upper())
    total = sum(letter_to_number(char) for char in clean_name if char in VOWELS)
    return reduce_to_digit(total)

def get_numerology(name: str, dob: str) -> dict:
    """Returns full numerology report: Life Path, Destiny, and Soul Urge numbers."""
    life_path = calculate_life_path_number(dob)
    destiny = calculate_destiny_number(name)
    soul_urge = calculate_soul_urge_number(name)

    return {
        "name": name,
        "dob": dob,
        "life_path_number": life_path,
        "destiny_number": destiny,
        "soul_urge_number": soul_urge,
        "summary": {
            "life_path": get_life_path_message(life_path),
            "destiny": f"Your destiny number {destiny} reflects your potential and talents.",
            "soul_urge": f"Your soul urge number {soul_urge} reveals your inner desires and motivations."
        }
    }

def get_life_path_message(n):
    messages = {
        1: "Leader, ambitious and driven.",
        2: "Peacemaker, sensitive and diplomatic.",
        3: "Creative and expressive communicator.",
        4: "Practical, grounded, and hardworking.",
        5: "Adventurous, adaptable, and curious.",
        6: "Nurturing, responsible, and community-oriented.",
        7: "Spiritual seeker and analytical thinker.",
        8: "Business-minded, powerful, and efficient.",
        9: "Compassionate, generous, and global thinker.",
        11: "Visionary, intuitive, and inspiring (Master Number).",
        22: "Master builder, practical visionary (Master Number).",
        33: "Spiritual teacher, healer, and guide (Master Number)."
    }
    return messages.get(n, "Unique life path.")
