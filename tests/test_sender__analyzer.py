import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from protocol_layer.sender_analyzer import SenderAnalyzer


test_sender = "security@fake-bank.com"

result = SenderAnalyzer.analyze(test_sender)

print("Sender Analysis Result:\n")
for key, value in result.items():
    print(f"{key}: {value}")