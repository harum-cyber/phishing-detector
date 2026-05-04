import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from preprocessing.email_parser import EmailParser


file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "sample_phishing.eml"))

result = EmailParser.parse_eml(file_path)

print("Subject:")
print(result["subject"])

print("\nSender:")
print(result["sender"])

print("\nBody:")
print(result["body"])