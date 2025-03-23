from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.transit import get_transits, get_daily_global_transits
from utils.match_logic import analyze_compatibility
from utils.kp_predictor import get_kp_prediction

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Navadharma Astrology API"}

# Input model for KP prediction
class KPRequest(BaseModel):
    name: str
    birthDate: str
    birthTime: str
    birthPlace: str

@app.post("/predict-kp")
def predict_kp(data: KPRequest):
    try:
        result = get_kp_prediction(
            name=data.name,
            birth_date=data.birthDate,
            birth_time=data.birthTime,
            birth_place=data.birthPlace
        )
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Input model for compatibility
class CompatibilityRequest(BaseModel):
    person1: dict
    person2: dict

@app.post("/compatibility")
def compatibility(data: CompatibilityRequest):
    try:
        result = analyze_compatibility(data.person1, data.person2)
        return {"compatibility": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Input model for transit request
class TransitRequest(BaseModel):
    birthDate: str
    birthTime: str
    birthPlace: str

@app.post("/transits")
def transit(data: TransitRequest):
    try:
        result = get_transits(data.birthDate, data.birthTime, data.birthPlace)
        return {"transits": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/daily-transits")
def daily_transits():
    try:
        result = get_daily_global_transits()
        return {"dailyTransits": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
