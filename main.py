from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.chart_extractor import extract_chart_details
from utils.dasha_calculator import get_current_dasha_periods
from utils.daily_forecast import get_daily_forecast
from utils.matchmaking import get_matchmaking_report

app = FastAPI()

# === Pydantic Schemas ===

class BirthDetails(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str

class ForecastRequest(BirthDetails):
    target_date: str = None

class MatchRequest(BaseModel):
    person1: BirthDetails
    person2: BirthDetails

# === ROUTES ===

@app.get("/")
def read_root():
    return {"message": "🪐 Navadharma Astrology API is live."}

@app.post("/get-chart")
def get_chart(details: BirthDetails):
    try:
        return extract_chart_details(
            details.name,
            details.date_of_birth,
            details.time_of_birth,
            details.place_of_birth
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-dasha")
def get_dasha(details: BirthDetails):
    try:
        return get_current_dasha_periods(
            details.date_of_birth,
            details.time_of_birth,
            details.place_of_birth
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/daily-forecast")
def daily_forecast(request: ForecastRequest):
    try:
        return get_daily_forecast(
            name=request.name,
            dob=request.date_of_birth,
            tob=request.time_of_birth,
            pob=request.place_of_birth,
            target_date=request.target_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/matchmaking")
def matchmaking(request: MatchRequest):
    try:
        return get_matchmaking_report(request.person1, request.person2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
