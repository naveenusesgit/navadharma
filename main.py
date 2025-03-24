from fastapi import FastAPI
from pydantic import BaseModel
from utils.kundli import (
    get_kundli_data,
    get_dasha_report,
    get_nakshatra_info,
    get_chart_data,
    get_matchmaking_report,
    get_panchang_data
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Navadharma Astrology API",
    description="Endpoints for generating kundli, dasha, nakshatra, charts, matchmaking and panchang.",
    version="1.0.0"
)

# Allow all origins (update in prod!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard input
class AstroRequest(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM (24-hour)
    place: str  # e.g., "Chennai, India"

class MatchRequest(BaseModel):
    boy_name: str
    boy_dob: str
    boy_tob: str
    boy_pob: str
    girl_name: str
    girl_dob: str
    girl_tob: str
    girl_pob: str


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "OK"}


@app.post("/generate-report")
def generate_report(req: AstroRequest):
    """Generates full kundli report (D1/D9 charts, lagna, nakshatra, etc)."""
    return get_kundli_data(req.name, req.date, req.time, req.place)


@app.post("/kundli-chart")
def kundli_chart(req: AstroRequest):
    """Returns D1/D9 chart data (planetary positions in houses/signs)."""
    return get_chart_data(req.name, req.date, req.time, req.place)


@app.post("/dasha")
def dasha(req: AstroRequest):
    """Returns Vimshottari Dasha timeline for the person."""
    return get_dasha_report(req.name, req.date, req.time, req.place)


@app.post("/nakshatra")
def nakshatra(req: AstroRequest):
    """Returns moon nakshatra and pada information."""
    return get_nakshatra_info(req.name, req.date, req.time, req.place)


@app.post("/matchmaking")
def matchmaking(req: MatchRequest):
    """Returns matchmaking report for two individuals."""
    return get_matchmaking_report(req)


@app.post("/panchang")
def panchang(req: AstroRequest):
    """Returns panchang data for given date and place (tithi, yoga, karana, etc)."""
    return get_panchang_data(req.date, req.time, req.place)
