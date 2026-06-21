import pandas as pd


RESULTS_PATH = "data/processed/full_test_results.csv"


def metrics(df):
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

df["expected"] = df["expected"].astype(str).str.lower().map({
    "true": True,
    "false": False,
    "1": True,
    "0": False
})

df["predicted"] = df["predicted"].astype(str).str.lower().map({
    "true": True,
    "false": False,
    "1": True,
    "0": False
})

print("\n=== Overall Metrics ===")
print(metrics(df))

print("\n=== Metrics by Source ===")
for source, group in df.groupby("source"):
    print("\nSource:", source)
    print(metrics(group))

print("\n=== Semantic Source Counts ===")
print(df["semantic_source"].value_counts())

print("\n=== Risk Distribution ===")
print(df["risk"].value_counts())

print("\n=== Risk Distribution for False Negatives ===")
fn_df = df[(df["expected"] == True) & (df["predicted"] == False)]
print(fn_df["risk"].value_counts())

print("\n=== Score Statistics for False Negatives ===")
print(fn_df["score"].describe())

print("\n=== Top FN Reasons ===")
print(fn_df["reason"].value_counts().head(20))