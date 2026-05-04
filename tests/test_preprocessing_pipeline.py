import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from preprocessing.email_parser import EmailParser
from preprocessing.html_cleaner import HTMLCleaner
from protocol_layer.url_analyzer import URLAnalyzer
from protocol_layer.sender_analyzer import SenderAnalyzer

file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "raw", "sample_phishing.eml")
)

email_data = EmailParser.parse_eml(file_path)
cleaned_data = HTMLCleaner.clean(email_data["body"])
sender_result = SenderAnalyzer.analyze(email_data["sender"])

url_results = []
for link in cleaned_data["links"]:
    url_results.append(URLAnalyzer.analyze(link))


# === CONSISTENCY CHECK ===
sender_domain = sender_result["domain"]

mismatch = False
for url in url_results:
    if sender_domain not in url["domain"]:
        mismatch = True


print("Subject:")
print(email_data["subject"])

print("\nSender:")
print(sender_result)

print("\nCleaned Body:")
print(cleaned_data["text"])

print("\nURL Analysis:")
for result in url_results:
    print(result)

print("\nDomain Mismatch:")
print(mismatch)