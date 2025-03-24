from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

def get_coordinates(place_name):
    """
    Returns (latitude, longitude) for a given place name using geopy.
    """
    geolocator = Nominatim(user_agent="navadharma_astrology")
    location = geolocator.geocode(place_name)
    if not location:
        raise ValueError(f"Location not found: {place_name}")
    return location.latitude, location.longitude

def get_timezone_name(lat, lon):
    """
    Returns timezone name (e.g. 'Asia/Kolkata') from coordinates using TimezoneFinder.
    """
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    if not tz_name:
        raise ValueError("Timezone not found for coordinates.")
    return tz_name

def get_timezone_offset(date_str, time_str, tz_name):
    """
    Returns UTC offset in hours for a given timezone and datetime string.
    """
    naive_dt = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
    tz = pytz.timezone(tz_name)
    localized_dt = tz.localize(naive_dt, is_dst=None)
    offset_hours = localized_dt.utcoffset().total_seconds() / 3600
    return offset_hours

def get_offset_from_place(date_str, time_str, place_name):
    """
    Full pipeline: from place name → coordinates → timezone → UTC offset
    """
    lat, lon = get_coordinates(place_name)
    tz_name = get_timezone_name(lat, lon)
    offset = get_timezone_offset(date_str, time_str, tz_name)
    return offset
