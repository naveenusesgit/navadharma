from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from utils.pdf_generator import generate_pdf
from utils.astro_logic import compute_full_astrology
from utils.gpt_summary import generate_gpt_summary

load_dotenv()  # Load .env if present

app = FastAPI()

# CORS settings (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key auth (optional, controlled via env)
API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

def verify_key(request: Request):
    key = request.headers.get("X-API-Key")
    if API_KEY and key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key.")

# Request model
class KPInput(BaseModel):
    name: str
    date: str
    time: str
    place: str
    pdf: bool = False

@app.get("/")
def home():
    return {"status": "Navadharma API is live 🌙"}

@app.post("/predict-kp")
def predict_kp(input_data: KPInput, request: Request = Depends(verify_key)):
    try:
        # 🔮 Step 1: Compute astrology logic
        report_data =
