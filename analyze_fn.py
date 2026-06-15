import pandas as pd

df = pd.read_csv("data/processed/ceas_sample_200_results.csv")

fn = df[
    (df["expected"] == True) &
    (df["predicted"] == False)
]

print("False Negatives:", len(fn))

cols = [
    "index",
    "risk",
    "score",
    "llm_confidence",
    "semantic_source",
    "reason"
]

print(fn[cols].to_string())