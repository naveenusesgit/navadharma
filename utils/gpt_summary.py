# utils/gpt_summary.py

import os
from typing import Optional

try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    openai_client = None

from utils.language_utils import translate_output


def generate_gpt_summary(text: str, lang: str = "en") -> str:
    """
    Generate a summary using OpenAI API or fallback to dummy summary.
    
    :param text: Input text to summarize
    :param lang: Language code (e.g., 'en', 'hi')
    :return: Summary string
    """
    summary = ""

    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Vedic astrologer."},
                    {"role": "user", "content": f"Summarize this kundli interpretation:\n{text}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = f"[Fallback Summary] {text[:200]}..."  # Truncate as fallback
    else:
        summary = f"[Demo Summary] {text[:200]}..."  # No OpenAI client

    return translate_output(summary, lang)
