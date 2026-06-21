import os
import sys
import time
import tempfile
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from main import run_pipeline


DATASET_PATH = os.path.join("data", "processed", "test_dataset.csv")
OUTPUT_PATH = os.path.join("data", "processed", "full_test_results.csv")

BATCH_SIZE = 25
SLEEP_SECONDS = 0.1


COLUMNS = [
    "index",
    "source",
    "expected",
    "predicted",
    "correct",
    "risk",
    "score",
    "llm_confidence",
    "semantic_source",
    "reason",
]


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


def append_results(rows):
    if not rows:
        return

    file_exists = os.path.exists(OUTPUT_PATH)

    pd.DataFrame(rows, columns=COLUMNS).to_csv(
        OUTPUT_PATH,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )


def calculate_metrics(results_df):
    valid_df = results_df[results_df["predicted"].notna()].copy()

    valid_df["expected"] = valid_df["expected"].astype(str).map({
        "True": True,
        "False": False,
        "1": True,
        "0": False,
        "true": True,
        "false": False,
    })

    valid_df["predicted"] = valid_df["predicted"].astype(str).map({
        "True": True,
        "False": False,
        "1": True,
        "0": False,
        "true": True,
        "false": False,
    })

    tp = len(valid_df[(valid_df["expected"] == True) & (valid_df["predicted"] == True)])
    tn = len(valid_df[(valid_df["expected"] == False) & (valid_df["predicted"] == False)])
    fp = len(valid_df[(valid_df["expected"] == False) & (valid_df["predicted"] == True)])
    fn = len(valid_df[(valid_df["expected"] == True) & (valid_df["predicted"] == False)])

    total = len(valid_df)
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("\n=== Final Metrics ===")
    print("Total valid:", total)
    print("TP:", tp)
    print("TN:", tn)
    print("FP:", fp)
    print("FN:", fn)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


def evaluate_full_test():
    df = pd.read_csv(DATASET_PATH)

    if os.path.exists(OUTPUT_PATH):
        existing_df = pd.read_csv(OUTPUT_PATH)
        processed_indexes = set(existing_df["index"].astype(int).tolist())
        print("Resuming from existing results...")
        print("Already processed:", len(processed_indexes))
    else:
        processed_indexes = set()
        print("Starting new evaluation...")

    total_rows = len(df)
    pending_rows = []

    try:
        for index, row in df.iterrows():
            if index in processed_indexes:
                continue

            temp_path = create_temp_eml(row)

            try:
                analysis = run_pipeline(temp_path)

                expected = bool(row["label"])
                predicted = analysis["decision"]["is_phishing"]

                result_row = {
                    "index": index,
                    "source": row.get("source", ""),
                    "expected": expected,
                    "predicted": predicted,
                    "correct": expected == predicted,
                    "risk": analysis["decision"]["risk"],
                    "score": analysis["decision"]["score"],
                    "llm_confidence": analysis["decision"].get("llm_confidence", 0),
                    "semantic_source": analysis["semantic_source"],
                    "reason": " | ".join(
                        str(r) for r in analysis["decision"]["reasons"][:5]
                    ),
                }

            except Exception as e:
                result_row = {
                    "index": index,
                    "source": row.get("source", ""),
                    "expected": bool(row["label"]),
                    "predicted": None,
                    "correct": False,
                    "risk": "error",
                    "score": 0,
                    "llm_confidence": 0,
                    "semantic_source": "error",
                    "reason": str(e),
                }

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            pending_rows.append(result_row)
            processed_indexes.add(index)

            if len(pending_rows) >= BATCH_SIZE:
                append_results(pending_rows)
                pending_rows = []

            print(f"Processed {len(processed_indexes)}/{total_rows} | index={index}")

            time.sleep(SLEEP_SECONDS)

    finally:
        append_results(pending_rows)

    final_df = pd.read_csv(OUTPUT_PATH)
    print("\nSaved:", OUTPUT_PATH)
    calculate_metrics(final_df)


if __name__ == "__main__":
    evaluate_full_test()