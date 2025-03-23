from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.kp_predictor import get_kp_prediction
from utils.chart_extractor import extract_chart

app = FastAPI()

# CORS middleware for ChatGPT or browser tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for both endpoints
class PredictionRequest(BaseModel):
    name: str
    birthDate: str
    birthTime: str
    birthPlace: str

class ChartRequest(BaseModel):
    birthDate: str
    birthTime: str
    birthPlace: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Navadharma Astrology API 🔮"}

@app.post("/predict-kp")
def predict_kp_route(req: PredictionRequest, api_key: str = Header(None)):
    if api_key != "kp-demo-secret-key-123456":
        return {"error": "Invalid or missing API key"}
    
    result = get_kp_prediction(req.name, req.birthDate, req.birthTime, req.birthPlace)
    return {"result": result}

@app.post("/get-chart")
def get_chart_details(req: ChartRequest):
    chart_data = extract_chart(req.birthDate, req.birthTime, req.birthPlace)
    return {"chart": chart_data}
