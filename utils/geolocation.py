from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_lat_lon_timezone(location):
    geolocator = Nominatim(user_agent="navadharma")
    loc = geolocator.geocode(location)
    if not loc:
        raise ValueError("Location not found")

    lat = loc.latitude
    lon = loc.longitude
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=lon, lat=lat)

    return lat, lon, timezone
