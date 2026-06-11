import json
from groq import Groq

from src.config import GROQ_API_KEY, GROQ_MODEL


class GroqSemanticAnalyzer:
    @staticmethod
    def analyze(subject, body, sender, links):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing")

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are a cybersecurity expert specialized in phishing email detection.

Analyze the email semantically. Focus only on language, intent, social engineering, urgency, threats, impersonation, and credential theft.

Return ONLY valid JSON with this exact schema:
{{
  "is_semantically_suspicious": true,
  "risk": "low|medium|high",
  "confidence": 0.0,
  "social_engineering_indicators": [],
  "credential_theft_indicators": [],
  "impersonation_indicators": [],
  "reason": "",
  "recommended_action": ""
}}

Email:
Subject: {subject}
Sender: {sender}
Links: {links}
Body: {body}
"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You output strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)