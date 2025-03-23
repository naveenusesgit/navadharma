from fastapi import FastAPI
from pydantic import BaseModel
from utils.astro_logic import analyze_chart, get_remedies, calculate_dasha, get_yogas, get_nakshatra_details
from utils.transit import get_transits, get_daily_global_transits
from utils.match_logic import analyze_compatibility
from utils.numerology import calculate_numerology
from utils.pdf_generator import generate_full_report, generate_match_report
from utils.gpt_summary import gpt_summary
from utils.gpt_chat import ChatSessionManager

app = FastAPI()
chat_manager = ChatSessionManager()

# Models
class UserInput(BaseModel):
    name: str
    dob: str  # format: YYYY-MM-DD
    tob: str  # format: HH:MM
    pob: str
    lang: str = "en"
    pdf: bool = False

class MatchInput(BaseModel):
    person1: UserInput
    person2: UserInput

class ChatInput(BaseModel):
    session_id: str
    message: str

# Endpoints

@app.post("/predict-kp")
async def predict_kp(user: UserInput):
    chart = analyze_chart(user.name, user.dob, user.tob, user.pob)
    dasha = calculate_dasha(chart)
    yogas = get_yogas(chart)
    nakshatra = get_nakshatra_details(chart)
    remedies = get_remedies(chart)
    gpt = gpt_summary(chart, lang=user.lang)
    pdf = None

    if user.pdf:
        pdf = generate_full_report(user.name, chart, dasha, yogas, nakshatra, remedies, gpt, lang=user.lang)

    return {
        "chart": chart,
        "dasha": dasha,
        "yogas": yogas,
        "nakshatra": nakshatra,
        "remedies": remedies,
        "gpt": gpt,
        "pdf": pdf
    }

@app.post("/transit")
async def get_transit(user: UserInput):
    transits = get_transits(user.dob, user.tob, user.pob)
    gpt = gpt_summary(transits, lang=user.lang)
    return {"transits": transits, "gpt": gpt}

@app.get("/daily-transit")
async def daily_transit():
    data = get_daily_global_transits()
    return data

@app.post("/numerology")
async def numerology(user: UserInput):
    return calculate_numerology(user.name, user.dob)

@app.post("/match-compatibility")
async def match_compatibility(match: MatchInput):
    result = analyze_compatibility(match.person1, match.person2)
    gpt = gpt_summary(result, lang=match.person1.lang)
    pdf = generate_match_report(result, gpt, match.person1, match.person2, lang=match.person1.lang)
    return {
        "matchReport": result,
        "gpt": gpt,
        "pdf": pdf
    }

@app.post("/gpt-chat")
async def gpt_chat(chat: ChatInput):
    response = chat_manager.chat(chat.session_id, chat.message)
    return {"response": response}
