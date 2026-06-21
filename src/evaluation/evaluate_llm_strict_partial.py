import pandas as pd


RESULTS_PATH = "data/processed/full_test_results_llm_strict.csv"


def to_bool(series):
    return series.astype(str).str.lower().map({
        "true": True,
        "false": False,
        "1": True,
        "0": False
    })


def calculate_metrics(df):
    tp = len(df[(df["expected"] == True) & (df["predicted"] == True)])
    tn = len(df[(df["expected"] == False) & (df["predicted"] == False)])
    fp = len(df[(df["expected"] == False) & (df["predicted"] == True)])
    fn = len(df[(df["expected"] == True) & (df["predicted"] == False)])

    total = len(df)

    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    return {
        "total": total,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


df = pd.read_csv(RESULTS_PATH)

df = df[df["semantic_source"] == "groq_llama"].copy()

df["expected"] = to_bool(df["expected"])
df["predicted"] = to_bool(df["predicted"])

print("\n=== Llama/Groq Strict Evaluation ===")
print("Rows evaluated by Llama:", len(df))

print("\n=== Class Distribution ===")
print(df["expected"].value_counts())

print("\n=== Overall Metrics ===")
overall = calculate_metrics(df)
for key, value in overall.items():
    print(f"{key}: {value}")

print("\n=== Metrics by Source ===")
rows = []

for source, group in df.groupby("source"):
    source_metrics = calculate_metrics(group)
    source_metrics["source"] = source
    rows.append(source_metrics)

    print("\nSource:", source)
    for key, value in source_metrics.items():
        print(f"{key}: {value}")

metrics_df = pd.DataFrame(rows)
metrics_df.to_csv(
    "data/processed/llm_strict_partial_metrics_by_source.csv",
    index=False,
    encoding="utf-8"
)

pd.DataFrame([overall]).to_csv(
    "data/processed/llm_strict_partial_overall_metrics.csv",
    index=False,
    encoding="utf-8"
)

print("\nSaved:")
print("data/processed/llm_strict_partial_overall_metrics.csv")
print("data/processed/llm_strict_partial_metrics_by_source.csv")