from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from utils.kp_predictor import get_kp_prediction
from utils.chart_extractor import extract_chart_details
from utils.daily_forecast import get_daily_forecast
from utils.matchmaking import match_compatibility
from utils.transit_analysis import analyze_transits

app = FastAPI()

class BirthDetails(BaseModel):
    name: str
    date_of_birth: str = Field(alias="dob")
    time_of_birth: str = Field(alias="tob")
    place_of_birth: str = Field(alias="pob")
    date: str | None = None  # Optional forecast date

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class MatchRequest(BaseModel):
    person1: BirthDetails
    person2: BirthDetails


@app.post("/predict-kp")
async def predict_kp(data: BirthDetails):
    try:
        return get_kp_prediction(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-chart")
async def get_chart(data: BirthDetails):
    try:
        return extract_chart_details(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/daily-forecast")
async def daily_forecast(data: BirthDetails):
    try:
        return get_daily_forecast(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/matchmaking")
async def matchmaking(data: MatchRequest):
    try:
        return match_compatibility(data.person1, data.person2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transit-analysis")
async def transit_analysis(data: BirthDetails):
    try:
        return analyze_transits(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
