import os
import sys
import tempfile
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from main import run_pipeline
from src.evaluation.protocol_only import ProtocolOnlyDecision
from src.evaluation.llm_only import LLMOnlyDecision


DATASET_PATH = os.path.join("data", "processed", "ceas_sample_200.csv")
OUTPUT_PATH = os.path.join("data", "processed", "model_comparison_results.csv")


def create_temp_eml(row):
    subject = str(row.get("subject", ""))
    sender = str(row.get("sender", ""))
    body = str(row.get("body", ""))

    eml_content = f"""From: {sender}
Subject: {subject}
MIME-Version: 1.0
Content-Type: text/html

{body}
"""

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".eml",
        mode="w",
        encoding="utf-8"
    )

    temp_file.write(eml_content)
    temp_file.close()

    return temp_file.name


def calculate_metrics(results, prediction_column):
    tp = len(results[(results["expected"] == True) & (results[prediction_column] == True)])
    tn = len(results[(results["expected"] == False) & (results[prediction_column] == False)])
    fp = len(results[(results["expected"] == False) & (results[prediction_column] == True)])
    fn = len(results[(results["expected"] == True) & (results[prediction_column] == False)])

    accuracy = (tp + tn) / len(results)
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    return {
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    }


def run_comparison():
    df = pd.read_csv(DATASET_PATH)

    rows = []

    for index, row in df.iterrows():
        temp_path = create_temp_eml(row)

        try:
            analysis = run_pipeline(temp_path)

            expected = bool(row["label"])

            protocol_prediction = ProtocolOnlyDecision.decide(
                analysis["sender"],
                analysis["urls"],
                analysis["mismatch"]
            )

            llm_prediction = LLMOnlyDecision.decide(
                analysis["semantic"]
            )

            hybrid_prediction = analysis["decision"]["is_phishing"]

            rows.append({
                "index": index,
                "expected": expected,
                "protocol_only": protocol_prediction,
                "llm_only": llm_prediction,
                "hybrid": hybrid_prediction,
                "hybrid_risk": analysis["decision"]["risk"],
                "hybrid_score": analysis["decision"]["score"],
                "llm_confidence": analysis["decision"].get("llm_confidence", 0),
                "semantic_source": analysis["semantic_source"],
            })

            print(f"Processed {index + 1}/{len(df)}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    results = pd.DataFrame(rows)

    results.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print("\nSaved:", OUTPUT_PATH)

    print("\n=== Protocol Only ===")
    print(calculate_metrics(results, "protocol_only"))

    print("\n=== Llama Only ===")
    print(calculate_metrics(results, "llm_only"))

    print("\n=== Hybrid ===")
    print(calculate_metrics(results, "hybrid"))


if __name__ == "__main__":
    run_comparison()