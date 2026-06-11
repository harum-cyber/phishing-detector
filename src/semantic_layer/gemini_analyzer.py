import json
from google import genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiSemanticAnalyzer:
    @staticmethod
    def analyze(subject, body, sender, links):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing")

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
You are a cybersecurity expert specialized in phishing email detection.

Analyze the email semantically and return ONLY valid JSON.

Email:
Subject: {subject}
Sender: {sender}
Links: {links}
Body: {body}

Return JSON with this schema:
{{
  "is_semantically_suspicious": true,
  "risk": "low|medium|high",
  "confidence": 0.0,
  "social_engineering_indicators": [],
  "credential_theft_indicators": [],
  "reason": "",
  "recommended_action": ""
}}
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)