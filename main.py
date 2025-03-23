from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from utils.match_logic import analyze_compatibility
import logging

app = FastAPI(
    title="Navadharma API",
    description="Match compatibility analysis API using astrology logic.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class PersonData(BaseModel):
    name: str = Field(..., example="Person A")
    date: str = Field(..., example="1990-05-20")
    time: str = Field(..., example="14:30")
    location: str = Field(..., example="New York, USA")

class MatchRequest(BaseModel):
    person1: PersonData
    person2: PersonData

class MatchResult(BaseModel):
    score: float
    comments: str

@app.get("/", tags=["Health"])
def root():
    return {"status": "OK", "message": "Navadharma API is running 🚀"}

@app.get("/match", response_model=MatchResult, tags=["Compatibility"])
def get_match(date1: str, date2: str):
    """
    Quick match using just birthdates.
    """
    try:
        jd1 = datetime.strptime(date1, "%Y-%m-%d").toordinal()
        jd2 = datetime.strptime(date2, "%Y-%m-%d").toordinal()
        logger.info(f"Calculating match for {jd1} and {jd2}")
        score, comments = analyze_compatibility(jd1, jd2)
        return MatchResult(score=score, comments=comments)
    except Exception as e:
        logger.exception("Error in GET /match")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/match", response_model=MatchResult, tags=["Compatibility"])
def post_match(request: MatchRequest):
    """
    Full compatibility match using structured input.
    """
    try:
        jd1 = datetime.strptime(request.person1.date, "%Y-%m-%d").toordinal()
        jd2 = datetime.strptime(request.person2.date, "%Y-%m-%d").toordinal()
        logger.info(f"POST match: {request.person1.name} vs {request.person2.name}")
        score, comments = analyze_compatibility(jd1, jd2)
        return MatchResult(score=score, comments=comments)
    except Exception as e:
        logger.exception("Error in POST /match")
        raise HTTPException(status_code=422, detail=str(e))

