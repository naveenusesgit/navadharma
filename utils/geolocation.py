# utils/geolocation.py

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_lat_lon_timezone(place: str):
    geolocator = Nominatim(user_agent="astro-api")
    location = geolocator.geocode(place)

    if not location:
        raise ValueError(f"Could not find location for: {place}")

    lat = location.latitude
    lon = location.longitude

    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)

    return {
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone
    }
