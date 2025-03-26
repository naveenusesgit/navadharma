import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Set this in env

# Basic keyword fallback
def fallback_detect_goal(prompt: str) -> str:
    prompt = prompt.lower()
    if any(word in prompt for word in ["marriage", "wedding", "love"]):
        return "marriage"
    if any(word in prompt for word in ["business", "startup", "launch"]):
        return "business"
    if any(word in prompt for word in ["travel", "journey", "trip"]):
        return "travel"
    if any(word in prompt for word in ["education", "study", "exam"]):
        return "education"
    if any(word in prompt for word in ["career", "job", "interview"]):
        return "career"
    return "business"  # Default fallback

# GPT-based detection
def detect_goal_from_prompt(prompt: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Classify the user's life goal into one word: marriage, business, travel, education, or career."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5
        )
        goal = completion.choices[0].message.content.strip().lower()
        return goal if goal in ["marriage", "business", "travel", "education", "career"] else fallback_detect_goal(prompt)
    except Exception as e:
        return fallback_detect_goal(prompt)
