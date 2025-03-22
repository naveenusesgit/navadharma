import openai
import os
from utils.astro_logic import analyze_chart
from utils.gpt_summary import gpt_summary

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatSessionManager:
    def __init__(self):
        self.sessions = {}

    def chat(self, session_id, user_message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

            # Try to auto-prime if chart details in first message
            chart_hint = self._detect_chart_info(user_message)
            if chart_hint:
                self.sessions[session_id].append({"role": "system", "content": chart_hint})

        self.sessions[session_id].append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.sessions[session_id],
            temperature=0.7
        )

        reply = response['choices'][0]['message']['content']
        self.sessions[session_id].append({"role": "assistant", "content": reply})
        return reply

    def _detect_chart_info(self, message: str) -> str:
        # Naive check for keywords
        keywords = ["dob", "tob", "pob", "date of birth", "time of birth", "place of birth"]
        if any(word in message.lower() for word in keywords):
            try:
                # Attempt to extract & process chart if format is right
                import re
                name = "User"
                dob_match = re.search(r"\d{2}-\d{2}-\d{4}", message)
                tob_match = re.search(r"\d{2}:\d{2}", message)
                pob_match = re.search(r"in\s+([a-zA-Z\s]+)", message)

                if dob_match and tob_match and pob_match:
                    dob = dob_match.group()
                    tob = tob_match.group()
                    pob = pob_match.group(1).strip()

                    chart = analyze_chart(name, dob, tob, pob)
                    summary = gpt_summary(chart)
                    return f"User provided their birth details: DOB: {dob}, TOB: {tob}, POB: {pob}. Here's a brief chart interpretation: {summary}"
            except Exception as e:
                return "User shared chart details, but couldn't parse."

        return ""
