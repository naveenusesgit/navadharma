from pydantic import BaseModel

class KundliRequest(BaseModel):
    datetime: str
    place: str
    latitude: float
    longitude: float
    timezone: float

class MonthlyRequest(BaseModel):
    rashi: str
    month: str = None

class WeeklyRequest(BaseModel):
    rashi: str
    week: str = None

class NumerologyRequest(BaseModel):
    name: str
    dob: str  # Format: YYYY-MM-DD
