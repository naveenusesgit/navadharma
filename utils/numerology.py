# utils/numerology.py

from datetime import datetime

def calculate_life_path_number(date_of_birth: str) -> int:
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    total = sum(int(char) for char in dob.strftime("%Y%m%d"))

    # Reduce to single digit (except 11, 22 which are master numbers)
    while total > 9 and total not in (11, 22):
        total = sum(int(d) for d in str(total))

    return total

def get_numerology_prediction(date_of_birth: str) -> dict:
    try:
        life_path = calculate_life_path_number(date_of_birth)
    except ValueError as e:
        return {"error": str(e)}

    predictions = {
        1: "You are a natural leader. This week is perfect for initiating new projects.",
        2: "Harmony and balance are key. Focus on relationships and partnerships.",
        3: "Creativity will shine. Good time for self-expression.",
        4: "Discipline and structure will benefit you. Focus on building a solid foundation.",
        5: "Expect change and excitement. Embrace flexibility.",
        6: "Nurturing energy surrounds you. Prioritize home and loved ones.",
        7: "Introspection brings clarity. Take time for spiritual pursuits.",
        8: "Success and ambition drive you. Focus on career goals.",
        9: "Compassion and service to others will bring fulfillment.",
        11: "You have strong intuition and insight. Follow your higher calling.",
        22: "You are a master builder. Your vision can manifest if you stay grounded."
    }

    message = predictions.get(life_path, "No prediction found.")
    return {
        "date_of_birth": date_of_birth,
        "life_path_number": life_path,
        "prediction": message
    }
