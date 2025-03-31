from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart
import swisseph as swe

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Navadharma KP API is live 🎉"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(...),
    month: int = Query(...),
    day: int = Query(...),
    hour: int = Query(...),
    minute: int = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    tz: float = Query(5.5),
    system: str = Query("kp", enum=["kp"])  # Forcing KP system
):
    # Convert local time to UTC
    utc_hour = hour + (minute / 60.0) - tz
    jd = swe.julday(year, month, day, utc_hour)
    
    return generate_kundli_chart(jd, latitude, longitude, tz=tz, system=system)
