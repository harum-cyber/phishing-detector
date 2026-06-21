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
OLD_RESULTS_PATH = os.path.join("data", "processed", "full_test_results_fallback_limited.csv")
FINAL_RESULTS_PATH = os.path.join("data", "processed", "full_test_results_llm_strict.csv")

SLEEP_SECONDS = 1
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
    file_exists = os.path.exists(FINAL_RESULTS_PATH)

    pd.DataFrame([row], columns=COLUMNS).to_csv(
        FINAL_RESULTS_PATH,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )


def prepare_final_file():
    if os.path.exists(FINAL_RESULTS_PATH):
        print("Final strict file already exists. Resuming...")
        return

    old_df = pd.read_csv(OLD_RESULTS_PATH)

    groq_df = old_df[old_df["semantic_source"] == "groq_llama"].copy()

    groq_df.to_csv(
        FINAL_RESULTS_PATH,
        index=False,
        encoding="utf-8"
    )

    print("Created strict result file using existing Groq results.")
    print("Initial Groq rows:", len(groq_df))


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
    valid_df = results_df[results_df["predicted"].notna()].copy()

    valid_df["expected"] = valid_df["expected"].astype(str).str.lower().map({
        "true": True,
        "false": False,
        "1": True,
        "0": False
    })

    valid_df["predicted"] = valid_df["predicted"].astype(str).str.lower().map({
        "true": True,
        "false": False,
        "1": True,
        "0": False
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

    print("\n=== Current Strict Metrics ===")
    print("Total valid:", total)
    print("TP:", tp)
    print("TN:", tn)
    print("FP:", fp)
    print("FN:", fn)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


def rerun_fallback_rows():
    prepare_final_file()

    dataset_df = pd.read_csv(DATASET_PATH)
    old_results_df = pd.read_csv(OLD_RESULTS_PATH)
    final_df = pd.read_csv(FINAL_RESULTS_PATH)

    processed_indexes = set(final_df["index"].astype(int).tolist())

    fallback_indexes = old_results_df[
        old_results_df["semantic_source"] == "rule_based_fallback"
    ]["index"].astype(int).tolist()

    remaining_indexes = [
        idx for idx in fallback_indexes
        if idx not in processed_indexes
    ]

    print("Total test rows:", len(dataset_df))
    print("Already strict Groq rows:", len(processed_indexes))
    print("Fallback rows to rerun:", len(remaining_indexes))

    for index in remaining_indexes:
        row = dataset_df.iloc[index]

        success = False

        for attempt in range(1, MAX_RETRIES_PER_EMAIL + 1):
            temp_path = create_temp_eml(row)

            try:
                analysis = run_pipeline(temp_path)

                if analysis["semantic_source"] == "groq_llama":
                    result_row = build_result_row(index, row, analysis)
                    append_result(result_row)
                    processed_indexes.add(index)
                    success = True

                    print(
                        f"Saved Groq result {len(processed_indexes)}/13960 | index={index}"
                    )
                    break

                else:
                    print(
                        f"Fallback returned at index={index}, attempt={attempt}. "
                        "Likely rate limit."
                    )

                    time.sleep(90)

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        if not success:
            print("\nStopping safely.")
            print("Reason: Groq did not return a valid result after retries.")
            print("Run the same script again later or tomorrow to resume.")
            break

        time.sleep(SLEEP_SECONDS)

    final_df = pd.read_csv(FINAL_RESULTS_PATH)

    print("\nSaved:", FINAL_RESULTS_PATH)
    print(final_df["semantic_source"].value_counts())
    calculate_metrics(final_df)


if __name__ == "__main__":
    rerun_fallback_rows()