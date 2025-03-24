from utils.match import generate_match_report
from pydantic import BaseModel


class BirthDetails(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str


def get_matchmaking_report(person1: BirthDetails, person2: BirthDetails):
    """
    This function wraps the actual matchmaking logic from match.py
    and exposes a clean interface for the FastAPI route.
    """
    return generate_match_report(
        person1.name, person1.date_of_birth, person1.time_of_birth, person1.place_of_birth,
        person2.name, person2.date_of_birth, person2.time_of_birth, person2.place_of_birth
    )
