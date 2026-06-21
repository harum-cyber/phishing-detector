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

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "full_test_results_openrouter_strict.csv"
)

REFUSED_PATH = os.path.join(
    "data",
    "processed",
    "openrouter_refused_rows.csv"
)

SLEEP_SECONDS = 0.5
MAX_RETRIES_PER_EMAIL = 3

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

REFUSED_COLUMNS = [
    "index",
    "source",
    "label",
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


def append_result(row):
    file_exists = os.path.exists(OUTPUT_PATH)

    pd.DataFrame([row], columns=COLUMNS).to_csv(
        OUTPUT_PATH,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )


def append_refused(row):
    file_exists = os.path.exists(REFUSED_PATH)

    pd.DataFrame([row], columns=REFUSED_COLUMNS).to_csv(
        REFUSED_PATH,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )


def build_result_row(index, row, analysis):
    expected = bool(row["label"])
    predicted = analysis["decision"]["is_phishing"]

    return {
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


def calculate_metrics(results_df):
    valid_df = results_df.copy()

    valid_df["expected"] = valid_df["expected"].astype(str).str.lower().map({
        "true": True,
        "false": False,
        "1": True,
        "0": False,
    })

    valid_df["predicted"] = valid_df["predicted"].astype(str).str.lower().map({
        "true": True,
        "false": False,
        "1": True,
        "0": False,
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

    print("\n=== Current OpenRouter Strict Metrics ===")
    print("Total valid:", total)
    print("TP:", tp)
    print("TN:", tn)
    print("FP:", fp)
    print("FN:", fn)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


def load_existing_indexes(path):
    if not os.path.exists(path):
        return set()

    df = pd.read_csv(path)

    if "index" not in df.columns:
        return set()

    return set(df["index"].astype(int).tolist())


def evaluate_openrouter_strict():
    print("Starting OpenRouter strict evaluation...")

    df = pd.read_csv(DATASET_PATH)

    processed_indexes = load_existing_indexes(OUTPUT_PATH)
    refused_indexes = load_existing_indexes(REFUSED_PATH)

    print("Already processed:", len(processed_indexes))
    print("Already refused:", len(refused_indexes))

    total_rows = len(df)

    for index, row in df.iterrows():
        if index in processed_indexes or index in refused_indexes:
            continue

        success = False
        last_reason = ""

        for attempt in range(1, MAX_RETRIES_PER_EMAIL + 1):
            temp_path = create_temp_eml(row)

            try:
                analysis = run_pipeline(temp_path)

                if analysis["semantic_source"] == "openrouter_llama":
                    result_row = build_result_row(index, row, analysis)
                    append_result(result_row)

                    processed_indexes.add(index)
                    success = True

                    print(
                        f"Saved {len(processed_indexes)}/{total_rows} | index={index}"
                    )
                    break

                else:
                    last_reason = analysis["semantic"].get("reason", "")

                    print(
                        f"Non-OpenRouter result at index={index}, "
                        f"attempt={attempt}. "
                        f"semantic_source={analysis['semantic_source']}"
                    )
                    print("Reason:")
                    print(last_reason)

                    time.sleep(30)

            except Exception as e:
                last_reason = str(e)
                print(f"Error at index={index}, attempt={attempt}: {e}")
                time.sleep(30)

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        if not success:
            refused_row = {
                "index": index,
                "source": row.get("source", ""),
                "label": row.get("label", ""),
                "reason": last_reason,
            }

            append_refused(refused_row)
            refused_indexes.add(index)

            print(f"Skipped refused row | index={index}")
            print("No fallback was saved. Continuing...")

        time.sleep(SLEEP_SECONDS)

    if os.path.exists(OUTPUT_PATH):
        final_df = pd.read_csv(OUTPUT_PATH)

        print("\nSaved:", OUTPUT_PATH)
        print(final_df["semantic_source"].value_counts())
        calculate_metrics(final_df)

    if os.path.exists(REFUSED_PATH):
        refused_df = pd.read_csv(REFUSED_PATH)
        print("\nRefused rows:", len(refused_df))
        print("Saved:", REFUSED_PATH)


if __name__ == "__main__":
    evaluate_openrouter_strict()