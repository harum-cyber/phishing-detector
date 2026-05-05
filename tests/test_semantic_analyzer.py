import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from semantic_layer.semantic_analyzer import SemanticAnalyzer


subject = "Urgent Account Verification"

body = "Your account will be suspended unless you verify now."

result = SemanticAnalyzer.analyze(subject, body)

print("Semantic Analysis Result:\n")
for key, value in result.items():
    print(f"{key}: {value}")