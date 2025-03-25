# utils/numerology.py

from datetime import datetime

def reduce_to_digit(n):
    """Reduces a number to a single digit or master number (11, 22, 33)."""
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_life_path_number(dob: str) -> int:
    """
    Calculate the Life Path Number from date of birth.
    dob: string in 'YYYY-MM-DD' format
    """
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

def get_numerology(name: str, dob: str) -> dict:
    """
    Main numerology function that returns life path number and message.
    """
    life_path = calculate_life_path_number(dob)

    messages = {
        1: "You are a natural leader, ambitious and driven.",
        2: "You are a peacemaker, sensitive and diplomatic.",
        3: "You are expressive, social, and creative.",
        4: "You are practical, disciplined, and grounded.",
        5: "You are adventurous, dynamic, and freedom-loving.",
        6: "You are responsible, nurturing, and harmonious.",
        7: "You are introspective, analytical, and spiritual.",
        8: "You are powerful, successful, and authoritative.",
        9: "You are compassionate, idealistic, and humanitarian.",
        11: "You are intuitive, visionary, and inspiring (Master Number).",
        22: "You are a master builder, practical visionary (Master Number).",
        33: "You are a master teacher, nurturing guide (Master Number).",
    }

    return {
        "name": name,
        "dob": dob,
        "life_path_number": life_path,
        "message": messages.get(life_path, "You have a unique path.")
    }
