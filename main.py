from fastapi import FastAPI
from pydantic import BaseModel
from utils.chart_extractor import get_nakshatra_info, get_ascendant
from utils.dasha_calculator import get_current_dasha
from utils.geolocation import get_lat_lon_timezone
from utils.kp_predictor import get_kp_prediction
from utils.forecast_logic import generate_daily_forecast
import swisseph as swe
import datetime

app = FastAPI()


class ChartRequest(BaseModel):
    name: str
    dob: str  # YYYY-MM-DD
    tob: str  # HH:MM (24h)
    pob: str  # Place of birth


@app.post("/get-chart")
def get_chart(data: ChartRequest):
    # Step 1: Get lat/lon and timezone
    lat, lon, tz_offset = get_lat_lon_timezone(data.pob)

    # Step 2: Parse datetime and convert to UTC
    dt_str = f"{data.dob} {data.tob}"
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    utc_dt = dt - datetime.timedelta(hours=tz_offset)

    # Step 3: Julian Day
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

    # Step 4: Moon & Ascendant
    moon_long = swe.calc_ut(jd, swe.MOON)[0]
    ascendant = get_ascendant(jd, lat, lon)
    nakshatra, pada, moon_sign = get_nakshatra_info(moon_long)

    # Step 5: Dasha
    dasha_info = get_current_dasha(jd, moon_long)

    return {
        "name": data.name,
        "moon_sign": moon_sign,
        "nakshatra": nakshatra,
        "pada": pada,
        "ascendant": ascendant,
        "current_dasha": dasha_info
    }


class KPPredictRequest(BaseModel):
    name: str
    dob: str
    tob: str
    pob: str
    question: str = "General prediction"


@app.post("/predict-kp")
def predict_kp(data: KPPredictRequest):
    return get_kp_prediction(data.name, data.dob, data.tob, data.pob, data.question)


class ForecastRequest(BaseModel):
    name: str
    dob: str
    tob: str
    pob: str
    date: str  # YYYY-MM-DD
    focus_area: str = "general"  # career, relationship, legal, etc.


@app.post("/daily-forecast")
def daily_forecast(data: ForecastRequest):
    return generate_daily_forecast(
        name=data.name,
        dob=data.dob,
        tob=data.tob,
        pob=data.pob,
        date=data.date,
        focus_area=data.focus_area
    )
