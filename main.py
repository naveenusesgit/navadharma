from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.chart_extractor import extract_chart_details
from utils.dasha_calculator import get_current_dasha
from utils.kp_predictor import get_kp_prediction
from utils.geolocation import get_lat_lon_timezone
from datetime import datetime
import pytz

app = FastAPI()

class BirthDetails(BaseModel):
    name: str
    date_of_birth: str  # Format: YYYY-MM-DD
    time_of_birth: str  # Format: HH:MM
    place_of_birth: str

@app.get("/")
def root():
    return {"message": "Welcome to Navadharma Astrology API"}

@app.post("/predict-kp")
def predict_kp(data: BirthDetails, request: Request):
    return get_kp_prediction(data)

@app.post("/get-chart")
def get_chart(data: BirthDetails):
    try:
        lat, lon, tz = get_lat_lon_timezone(data.place_of_birth)
        dt_str = f"{data.date_of_birth} {data.time_of_birth}"
        tzinfo = pytz.timezone(tz)
        dt_obj = tzinfo.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))

        chart = extract_chart_details(dt_obj, lat, lon)
        dasha = get_current_dasha(chart["julian_day"], chart["moon_longitude"], base_date=dt_obj)

        return {
            "name": data.name,
            "date_time": dt_obj.isoformat(),
            "location": {
                "place": data.place_of_birth,
                "latitude": lat,
                "longitude": lon,
                "timezone": tz,
            },
            "rasi": chart["rasi"],
            "nakshatra": chart["nakshatra"],
            "pada": chart["pada"],
            "lagna": chart["lagna"],
            "dasha": dasha,
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/daily-forecast")
def daily_forecast(data: BirthDetails):
    try:
        lat, lon, tz = get_lat_lon_timezone(data.place_of_birth)
        dt_str = f"{data.date_of_birth} {data.time_of_birth}"
        tzinfo = pytz.timezone(tz)
        dt_obj = tzinfo.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))

        chart = extract_chart_details(dt_obj, lat, lon)
        dasha = get_current_dasha(chart["julian_day"], chart["moon_longitude"], base_date=dt_obj)

        maha = dasha.get("current_maha_dasha", "")
        antar = dasha.get("current_antar_dasha", "")
        rasi = chart.get("rasi")
        nakshatra = chart.get("nakshatra")
        lagna = chart.get("lagna")

        message = (
            f"🌞 Daily Forecast for {data.name}\n"
            f"• Moon Sign (Rasi): {rasi}\n"
            f"• Nakshatra: {nakshatra}\n"
            f"• Lagna: {lagna}\n"
            f"• Current Dasha: {maha} → Antar Dasha: {antar}\n\n"
            f"✨ Based on your personalized Dasha period, today's energies are influenced by the karmic triggers of {maha} and the emotional tones of {antar}. "
            f"Use this time for spiritual alignment, careful decision-making, and emotional clarity."
        )

        return {
            "forecast": message,
            "rasi": rasi,
            "nakshatra": nakshatra,
            "lagna": lagna,
            "dasha": dasha
        }
    except Exception as e:
        return {"error": str(e)}
