import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from match import run_matchmaking
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any


class MatchmakingRequest(BaseModel):
    male_details: dict
    female_details: dict


def get_matchmaking_report(data: MatchmakingRequest) -> Any:
    try:
        male = data.male_details
        female = data.female_details

        result = run_matchmaking(male, female)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
