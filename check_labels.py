import pandas as pd

df = pd.read_csv(r"..\archive\CEAS_08.csv")

print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print("\nLabel counts:")
print(df["label"].value_counts())

print("\nURLs counts:")
print(df["urls"].value_counts().head(10))

print("\nSample rows:")
print(df[["sender", "subject", "label", "urls"]].head())