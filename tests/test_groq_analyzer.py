import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.semantic_layer.groq_analyzer import GroqSemanticAnalyzer

result = GroqSemanticAnalyzer.analyze(
    subject="Urgent Account Verification",
    body="Your account will be suspended unless you verify your account now.",
    sender="security@fake-bank.com",
    links=["http://fake-bank-login.com"],
)

print(result)