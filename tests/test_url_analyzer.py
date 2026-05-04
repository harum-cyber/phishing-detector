import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from protocol_layer.url_analyzer import URLAnalyzer


test_url = "http://fake-bank-login.com"

result = URLAnalyzer.analyze(test_url)

print("URL Analysis Result:\n")
for key, value in result.items():
    print(f"{key}: {value}")