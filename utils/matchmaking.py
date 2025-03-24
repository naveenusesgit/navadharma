import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from match import run_matchmaking
from pydantic import BaseModel


class BirthDetails(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str


def get_matchmaking_report(person1: BirthDetails, person2: BirthDetails):
    """
    Entry point for matchmaking report.
    Calls run_matchmaking from match.py using two birth profiles.
    """
    return run_matchmaking(
        person1.name, person1.date_of_birth, person1.time_of_birth, person1.place_of_birth,
        person2.name, person2.date_of_birth, person2.time_of_birth, person2.place_of_birth,
    )
