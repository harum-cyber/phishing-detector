import os
import sys 

from src.preprocessing.email_parser import EmailParser
from src.preprocessing.html_cleaner import HTMLCleaner
from src.protocol_layer.url_analyzer import URLAnalyzer
from src.protocol_layer.sender_analyzer import SenderAnalyzer
from src.semantic_layer.semantic_analyzer import SemanticAnalyzer
from src.decision_engine.rule_based_decision import RuleBasedDecision


def run_pipeline(file_path):

    # --- Parse Email ---
    email_data = EmailParser.parse_eml(file_path)

    # --- Clean HTML ---
    cleaned_data = HTMLCleaner.clean(email_data["body"])

    # --- Semantic Analysis ---
    semantic_result = SemanticAnalyzer.analyze(
        email_data["subject"],
        cleaned_data["text"]
    )

    # --- Sender Analysis ---
    sender_result = SenderAnalyzer.analyze(email_data["sender"])

    # --- URL Analysis ---
    url_results = []
    for link in cleaned_data["links"]:
        url_results.append(URLAnalyzer.analyze(link))

    # --- Domain Mismatch ---
    sender_domain = sender_result["domain"]
    mismatch = False

    for url in url_results:
        if sender_domain not in url["domain"]:
            mismatch = True

    # --- Final Decision ---
    decision = RuleBasedDecision.decide(
        sender_result,
        url_results,
        mismatch,
        semantic_result
    )

    return {
        "email": email_data,
        "cleaned": cleaned_data,
        "semantic": semantic_result,
        "sender": sender_result,
        "urls": url_results,
        "mismatch": mismatch,
        "decision": decision
    }

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <email_file>")
        sys.exit()

    email_filename = sys.argv[1]

    file_path = os.path.join(
        "data",
        "raw",
        email_filename
    )

    result = run_pipeline(file_path)

    print("\n=== FINAL RESULT ===\n")

    print("Subject:", result["email"]["subject"])
    print("Sender:", result["email"]["sender"])

    print("\nDecision:")
    print(result["decision"])