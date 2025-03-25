from fastapi import FastAPI
from utils.kundli import (
    get_dasha_periods,
    get_lagna_info,
    get_planetary_aspects,
    get_nakshatra_prediction,
    get_transit_effects,
    generate_kundli_report,
    generate_daily_prediction,
    get_matchmaking_report,
    get_numerology_report,
    get_remedies,
    get_divisional_charts
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Navadharma Jyotish API!"}


@app.get("/dasha")
def dasha_periods(name: str, date: str, time: str, place: str):
    return get_dasha_periods(name, date, time, place)


@app.get("/lagna")
def lagna_info(name: str, date: str, time: str, place: str):
    return get_lagna_info(name, date, time, place)


@app.get("/aspects")
def planetary_aspects(name: str, date: str, time: str, place: str):
    return get_planetary_aspects(name, date, time, place)


@app.get("/nakshatra")
def nakshatra_prediction(name: str, date: str, time: str, place: str):
    return get_nakshatra_prediction(name, date, time, place)


@app.get("/transits")
def transits(name: str, date: str, time: str, place: str):
    return get_transit_effects(name, date, time, place)


@app.get("/daily-prediction")
def daily_prediction(name: str, date: str, time: str, place: str):
    return generate_daily_prediction(name, date, time, place)


@app.get("/kundli-report")
def kundli_report(name: str, date: str, time: str, place: str):
    return generate_kundli_report(name, date, time, place)


@app.get("/matchmaking")
def matchmaking(person1: str, person2: str):
    return get_matchmaking_report(person1, person2)


@app.get("/numerology")
def numerology(name: str, birthdate: str):
    return get_numerology_report(name, birthdate)


@app.get("/remedies")
def remedies(name: str, date: str, time: str, place: str):
    return get_remedies(name, date, time, place)


@app.get("/charts")
def divisional_charts(name: str, date: str, time: str, place: str):
    return get_divisional_charts(name, date, time, place)
