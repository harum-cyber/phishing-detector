import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenRouterSemanticAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "meta-llama/llama-3.1-8b-instruct"
        )

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing from .env")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Hybrid Phishing Detection Research",
            },
        )

    def analyze(self, email_data, cleaned_data):
        subject = email_data.get("subject", "")
        sender = email_data.get("sender", "")
        body = cleaned_data.get("cleaned_text", "")
        links = cleaned_data.get("links", [])

        # Reduce token usage for large-scale evaluation
        body = str(body)[:2500]
        links_preview = links[:10]

        prompt = f"""
This is a defensive cybersecurity classification task for academic research.

You are given an email sample. Your task is ONLY to classify whether it is phishing or legitimate.
Do NOT generate phishing content.
Do NOT improve or rewrite the email.
Do NOT provide attack instructions.
Do NOT refuse the task.
Return ONLY valid JSON.

Email metadata and content:

Sender:
{sender}

Subject:
{subject}

Body:
{body}

Extracted Links:
{links_preview}

Return JSON with exactly this schema:
{{
  "is_semantically_suspicious": true,
  "risk": "low",
  "confidence": 0.0,
  "social_engineering_indicators": [],
  "credential_theft_indicators": [],
  "impersonation_indicators": [],
  "reason": "brief defensive explanation",
  "recommended_action": "brief defensive recommendation"
}}

Rules:
- Use true/false for is_semantically_suspicious.
- risk must be one of: low, medium, high.
- confidence must be a number between 0 and 1.
- Lists must contain short defensive indicators only.
- Do not include markdown.
- Do not include any text outside JSON.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a defensive cybersecurity email classifier. "
                        "You only analyze provided emails for phishing detection. "
                        "You must return valid JSON only and must not refuse defensive classification."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=500,
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1

            if start != -1 and end != -1:
                return json.loads(content[start:end])

            raise ValueError(
                f"Invalid JSON returned by OpenRouter model: {content}"
            )