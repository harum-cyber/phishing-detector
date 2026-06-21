import pandas as pd

files = [
    r"..\archive\CEAS_08.csv",
    r"..\archive\SpamAssasin.csv",
    r"..\archive\Nazario.csv",
]

for file in files:
    print("\n======================")
    print(file)

    df = pd.read_csv(file)

    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    if "label" in df.columns:
        print("Label counts:")
        print(df["label"].value_counts())

    print(df.head(2))