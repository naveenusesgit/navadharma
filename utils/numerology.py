# utils/numerology.py

def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:  # master numbers
        n = sum(int(d) for d in str(n))
    return n

def get_life_path(date_str):
    parts = date_str.split("-")
    digits = "".join(parts)
    return reduce_to_single_digit(sum(int(d) for d in digits))

def get_destiny_number(name):
    pythagorean = {
        "A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,
        "J":1,"K":2,"L":3,"M":4,"N":5,"O":6,"P":7,"Q":8,"R":9,
        "S":1,"T":2,"U":3,"V":4,"W":5,"X":6,"Y":7,"Z":8
    }
    name = name.upper().replace(" ", "")
    total = sum(pythagorean.get(char, 0) for char in name)
    return reduce_to_single_digit(total)

def numerology_profile(name, dob):
    life_path = get_life_path(dob)
    destiny = get_destiny_number(name)
    return {
        "lifePathNumber": life_path,
        "destinyNumber": destiny,
        "luckyNumbers": [life_path, destiny, life_path + destiny]
    }
