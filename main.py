import os
import sys 

from src.preprocessing.email_parser import EmailParser
from src.preprocessing.html_cleaner import HTMLCleaner
from src.protocol_layer.url_analyzer import URLAnalyzer
from src.protocol_layer.sender_analyzer import SenderAnalyzer
from src.semantic_layer.groq_analyzer import GroqSemanticAnalyzer
from src.semantic_layer.semantic_analyzer import SemanticAnalyzer
from src.fusion_engine.risk_fusion import RiskFusion


def run_pipeline(file_path):

    # --- Parse Email ---
    email_data = EmailParser.parse_eml(file_path)

    # --- Clean HTML ---
    cleaned_data = HTMLCleaner.clean(email_data["body"])

    # --- LLM Semantic Analysis ---
    try:
        semantic_result = GroqSemanticAnalyzer.analyze(
            email_data["subject"],
            cleaned_data["text"],
            email_data["sender"],
            cleaned_data["links"]
        )
        semantic_source = "groq_llama"
    except Exception as e:
        semantic_result = SemanticAnalyzer.analyze(
            email_data["subject"],
            cleaned_data["text"]
        )
        semantic_result = {
            "is_semantically_suspicious": semantic_result["semantic_risk"] != "low",
            "risk": semantic_result["semantic_risk"],
            "confidence": 0.0,
            "social_engineering_indicators": semantic_result["semantic_reasons"],
            "credential_theft_indicators": [],
            "impersonation_indicators": [],
            "reason": f"Fallback rule-based semantic analysis used. Error: {str(e)}",
            "recommended_action": ""
        }
        semantic_source = "rule_based_fallback"

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
    protocol_result = {
        "sender": sender_result,
        "urls": url_results,
        "mismatch": mismatch
    }

    decision = RiskFusion.decide(
        protocol_result,
        semantic_result
    )

    return {
        "email": email_data,
        "cleaned": cleaned_data,
        "semantic": semantic_result,
        "sender": sender_result,
        "urls": url_results,
        "mismatch": mismatch,
        "decision": decision,
        "semantic_source": semantic_source,
        "protocol": protocol_result,
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