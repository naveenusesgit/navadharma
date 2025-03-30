from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart
import swisseph as swe

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Navadharma KP API is live 🎯"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(...),
    month: int = Query(...),
    day: int = Query(...),
    hour: int = Query(12),
    minute: int = Query(0),
    second: int = Query(0),
    latitude: float = Query(...),
    longitude: float = Query(...),
    tz: float = Query(5.5)
):
    return generate_kundli_chart(year, month, day, hour, minute, second, latitude, longitude, tz)
