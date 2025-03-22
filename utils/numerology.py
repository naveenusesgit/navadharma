def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:  # Master numbers
        n = sum(int(d) for d in str(n))
    return n

def get_life_path_number(dob: str):
    parts = [int(p) for p in dob.split("-")]  # YYYY-MM-DD
    total = sum(int(d) for d in str(parts[0]) + str(parts[1]) + str(parts[2]))
    return reduce_to_single_digit(total)

def get_name_number(name):
    name = name.upper().replace(" ", "")
    numerology_map = {
        'A':1,'B':2,'C':3,'D':4,'E':5,'F':8,'G':3,'H':5,'I':1,
        'J':1,'K':2,'L':3,'M':4,'N':5,'O':7,'P':8,'Q':1,'R':2,
        'S':3,'T':4,'U':6,'V':6,'W':6,'X':5,'Y':1,'Z':7
    }
    return reduce_to_single_digit(sum(numerology_map.get(char, 0) for char in name))

def get_numerology_summary(name, dob):
    return {
        "life_path": get_life_path_number(dob),
        "destiny": get_name_number(name),
    }
