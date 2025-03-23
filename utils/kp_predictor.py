from utils.geolocation import get_lat_lon_timezone
from datetime import datetime

def get_kp_prediction(name: str, birth_date: str, birth_time: str, birth_place: str):
    # Get coordinates and timezone
    lat, lon, timezone = get_lat_lon_timezone(birth_place)
    
    # Format full datetime string
    dt_str = f"{birth_date} {birth_time}"
    birth_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    
    # Dummy prediction for now
    prediction = f"Hello {name}, based on your birth details at {birth_place}, KP astrology says your period is stable and positive."
    
    return {
        "name": name,
        "birthDate": birth_date,
        "birthTime": birth_time,
        "birthPlace": birth_place,
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone,
        "prediction": prediction
    }
