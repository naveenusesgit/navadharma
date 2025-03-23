from fastapi import FastAPI
from pydantic import BaseModel
from utils.kp_predictor import get_kp_prediction
from utils.chart_extractor import extract_chart
from utils.forecast import get_daily_forecast

app = FastAPI()


class KpRequest(BaseModel):
    name: str
    birthDate: str
    birthTime: str
    birthPlace: str


class ChartRequest(BaseModel):
    birthDate: str
    birthTime: str
    birthPlace: str


class ForecastRequest(BaseModel):
    birthDate: str
    birthTime: str
    birthPlace: str
    targetDate: str  # e.g. "2025-03-25"


@app.post("/predict-kp")
def predict_kp(req: KpRequest):
    result = get_kp_prediction(req.name, req.birthDate, req.birthTime, req.birthPlace)
    return {"prediction": result}


@app.post("/get-chart")
def get_chart(req: ChartRequest):
    chart_data = extract_chart(req.birthDate, req.birthTime, req.birthPlace)
    return chart_data


@app.post("/daily-forecast")
def daily_forecast(req: ForecastRequest):
    result = get_daily_forecast(
        birth_date=req.birthDate,
        birth_time=req.birthTime,
        birth_place=req.birthPlace,
        target_date=req.targetDate
    )
    return {"forecast": result}
