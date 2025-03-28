from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from utils.kundli import (
    get_planet_positions,
    get_ascendant_info,
    get_house_mapping,
    get_moon_info
)

app = FastAPI(title="Navadharma Jyotish API")

# 📌 Request Schema
class KundliRequest(BaseModel):
    datetime: str
    latitude: float
    longitude: float
    timezone: float

# ✅ GET PLANET POSITIONS
@app.post("/planet-positions")
def planet_positions(data: KundliRequest):
    return {
        "planet_positions": get_planet_positions(
            data.datetime,
            data.latitude,
            data.longitude,
            data.timezone
        )
    }

# ✅ GET ASCENDANT / LAGNA
@app.post("/lagna-info")
def lagna_info(data: KundliRequest):
    return {
        "ascendant": get_ascendant_info(
            data.datetime,
            data.latitude,
            data.longitude,
            data.timezone
        )
    }

# ✅ GET NAKSHATRA DETAILS
@app.post("/nakshatra-details")
def nakshatra_details(data: KundliRequest):
    return {
        "moon_nakshatra": get_moon_info(
            data.datetime,
            data.latitude,
            data.longitude,
            data.timezone
        )
    }

# ✅ GET FULL KUNDLI CHART
@app.post("/get-kundli-chart")
def kundli_chart(data: KundliRequest):
    return {
        "ascendant": get_ascendant_info(
            data.datetime,
            data.latitude,
            data.longitude,
            data.timezone
        ),
        "houses": get_house_mapping(
            data.datetime,
            data.latitude,
            data.longitude,
            data.timezone
        )
    }

# ✅ MOON INFO (RASI, NAKSHATRA, PADA)
@app.post("/moon-info")
def moon_info(data: KundliRequest):
    return get_moon_info(
        data.datetime,
        data.latitude,
        data.longitude,
        data.timezone
    )
