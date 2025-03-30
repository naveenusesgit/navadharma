from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart
import swisseph as swe

app = FastAPI(
    title="Navadharma KP API",
    description="Accurate KP astrology chart generator with Sub Lords, Nakshatras, and House Cusps.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Navadharma KP API is live 🎉"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(..., description="Hour of birth (24h format)"),
    minute: int = Query(0, description="Minute of birth"),
    latitude: float = Query(..., description="Latitude of birthplace"),
    longitude: float = Query(..., description="Longitude of birthplace")
):
    """
    Generate an accurate KP-based Kundli chart using Swiss Ephemeris.
    """
    return generate_kundli_chart(year, month, day, hour, minute, latitude, longitude)
