import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_summary(data: dict) -> str:
    prompt = f"""
You are a Vedic astrologer. Based on this data, write a 3-4 sentence summary in a wise tone:

Date: {data.get("date")}
Time: {data.get("time")}
Place: {data.get("place")}
Lagna: {data.get("lagna")}
Dasha: {data.get("currentDasha")}
Yogas: {data.get("yogas")}
Nakshatras: {data.get("nakshatras")}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Vedic astrologer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
