from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from utils.astro_logic import analyze_chart
from utils.transit import get_transits
from utils.match_logic import analyze_match
from utils.numerology import analyze_numerology
from utils.gpt_summary import generate_gpt_summary
from utils.gpt_chat import chat_with_gpt
import uuid
import os

app = FastAPI()

# CORS for frontend / Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment key
REQUIRED_API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

# Request schema
class KPRequest(BaseModel):
    name: str
    date: str
    time: str
    place: str
    language: str = "en"
    pdf: bool = False

class MatchRequest(BaseModel):
    person1: dict
    person2: dict
    language: str = "en"
    pdf: bool = False

class ChatRequest(BaseModel):
    message: str
    session_id: str
    language: str = "en"

# API Key validator
def validate_key(x_api_key: str = Header(...)):
    if x_api_key != REQUIRED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

# Main prediction route
@app.post("/predict-kp")
def predict_kp(data: KPRequest, x_api_key: str = Header(...)):
    validate_key(x_api_key)
    analysis = analyze_chart(data.dict())
    summary = generate_gpt_summary(analysis, lang=data.language)
    numerology = analyze_numerology(data.name, data.date)

    response = {
        "name": data.name,
        "analysis": analysis,
        "summary": summary,
        "numerology": numerology,
        "pdf": None
    }

    if data.pdf:
        report_data = {**data.dict(), **analysis, "summary": summary, "numerology": numerology}
        pdf_path = generate_pdf(report_data, filename=f"{data.name}_report.pdf")
        response["pdf"] = pdf_path

    return response

# Match compatibility
@app.post("/match-compatibility")
def match_compat(data: MatchRequest, x_api_key: str = Header(...)):
    validate_key(x_api_key)
    match_report = analyze_match(data.person1, data.person2, lang=data.language)
    pdf_url = None

    if data.pdf:
        from utils.pdf_generator import generate_match_pdf
        pdf_url = generate_match_pdf(data.person1, data.person2, match_report)

    return {
        "match": match_report,
        "pdf": pdf_url
    }

# Daily transit
@app.get("/daily-transit")
def transit(x_api_key: str = Header(...)):
    validate_key(x_api_key)
    return get_transits()

# GPT Chatbot
@app.post("/chat")
def chat(data: ChatRequest, x_api_key: str = Header(...)):
    validate_key(x_api_key)
    reply = chat_with_gpt(data.message, session_id=data.session_id, lang=data.language)
    return {"reply": reply}
