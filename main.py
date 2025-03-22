{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from fastapi import FastAPI, Request, HTTPException\
from pydantic import BaseModel\
from typing import Optional\
import os\
\
app = FastAPI()\
\
API_KEY = os.getenv("API_KEY", "kp-demo-secret-key-123456")\
\
\
class KPInput(BaseModel):\
    date: str  # YYYY-MM-DD\
    time: str  # HH:MM\
    place: str  # City, Country\
\
\
@app.get("/")\
def read_root():\
    return \{\
        "message": "
\f1 \uc0\u55357 \u56395 
\f0  Welcome to the KP Predictor API! Use POST /predict-kp to get detailed Vedic astrology predictions using the KP system."\
    \}\
\
\
@app.post("/predict-kp")\
def predict_kp(request: Request, data: KPInput):\
    auth = request.headers.get("Authorization")\
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != API_KEY:\
        raise HTTPException(status_code=401, detail="Unauthorized")\
\
    # 
\f1 \uc0\u55357 \u56622 
\f0  Dummy prediction logic (replace later with real KP engine)\
    response = \{\
        "lagna": "Aries",\
        "currentDasha": \{\
            "mahadasha": "Venus",\
            "antardasha": "Saturn",\
            "period": "2023-08-01 to 2026-05-15"\
        \},\
        "predictions": \{\
            "marriage": \{\
                "likely": True,\
                "window": "2024\'962025",\
                "explanation": "Venus is sub-lord of 7th house and active in Dasha"\
            \},\
            "career": \{\
                "change": False,\
                "explanation": "10th lord is stable and unaffected by transit"\
            \}\
        \}\
    \}\
\
    return response\
}