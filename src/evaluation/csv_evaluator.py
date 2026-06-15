import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)
import pandas as pd
import tempfile

from main import run_pipeline


DATASET_PATH = os.path.join("data", "processed", "ceas_sample_200.csv")
OUTPUT_PATH = os.path.join("data", "processed", "ceas_sample_200_results.csv")


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


def evaluate_csv():
    df = pd.read_csv(DATASET_PATH)

    results = []

    for index, row in df.iterrows():
        temp_path = create_temp_eml(row)

        try:
            analysis = run_pipeline(temp_path)

            expected = bool(row["label"])
            predicted = analysis["decision"]["is_phishing"]

            results.append({
                "index": index,
                "expected": expected,
                "predicted": predicted,
                "correct": expected == predicted,
                "risk": analysis["decision"]["risk"],
                "score": analysis["decision"]["score"],
                "semantic_source": analysis["semantic_source"],
                "llm_confidence": analysis["decision"].get("llm_confidence", 0),
                "reason": " | ".join(str(reason) for reason in analysis["decision"]["reasons"][:5]),
            })

            print(f"Processed {index + 1}/{len(df)}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print("Saved results:", OUTPUT_PATH)

    tp = len(results_df[(results_df["expected"] == True) & (results_df["predicted"] == True)])
    tn = len(results_df[(results_df["expected"] == False) & (results_df["predicted"] == False)])
    fp = len(results_df[(results_df["expected"] == False) & (results_df["predicted"] == True)])
    fn = len(results_df[(results_df["expected"] == True) & (results_df["predicted"] == False)])

    accuracy = (tp + tn) / len(results_df)
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("\n=== Metrics ===")
    print("TP:", tp)
    print("TN:", tn)
    print("FP:", fp)
    print("FN:", fn)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


if __name__ == "__main__":
    evaluate_csv()