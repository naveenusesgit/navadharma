from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.kundli import generate_kundli_report, get_kundli_chart, get_dasha_periods, get_nakshatra_info
from utils.panchang import get_panchang_data
from utils.matchmaking import get_matchmaking_report
from utils.transit import get_transit_info
from utils.ashtakvarga import get_ashtakvarga_analysis
from utils.muhurta import get_muhurta_suggestions
from utils.remedies import get_astrological_remedies

app = FastAPI()


# Base input model
class BirthDetails(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str


# Matchmaking input model
class MatchmakingInput(BaseModel):
    person1: BirthDetails
    person2: BirthDetails


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate-report")
def generate_astro_report(details: BirthDetails):
    try:
        return generate_kundli_report(details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/kundli-chart")
def kundli_chart(details: BirthDetails):
    return get_kundli_chart(details)


@app.post("/dasha")
def dasha_periods(details: BirthDetails):
    return get_dasha_periods(details)


@app.post("/nakshatra")
def nakshatra_info(details: BirthDetails):
    return get_nakshatra_info(details)


@app.post("/panchang")
def panchang_data(details: BirthDetails):
    return get_panchang_data(details)


@app.post("/matchmaking")
def matchmaking(data: MatchmakingInput):
    return get_matchmaking_report(data.person1, data.person2)


@app.post("/transits")
def transits(details: BirthDetails):
    return get_transit_info(details)


@app.post("/ashtakvarga")
def ashtakvarga(details: BirthDetails):
    return get_ashtakvarga_analysis(details)


@app.post("/muhurta")
def muhurta(details: BirthDetails):
    return get_muhurta_suggestions(details)


@app.post("/remedies")
def remedies(details: BirthDetails):
    return get_astrological_remedies(details)
