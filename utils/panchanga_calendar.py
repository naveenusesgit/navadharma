from datetime import datetime, timedelta
from utils.panchanga import get_panchanga

def generate_panchanga_calendar(start_date_str, days, latitude, longitude, timezone_offset):
    calendar = []

    start_dt = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
    for i in range(days):
        current_dt = start_dt + timedelta(days=i)
        iso_date = current_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        panchanga = get_panchanga(iso_date, latitude, longitude, timezone_offset)
        calendar.append({
            "date": current_dt.strftime("%Y-%m-%d"),
            "panchanga": panchanga
        })

    return calendar
