import os
import pandas as pd


RAW_PATH = r"..\archive\CEAS_08.csv"
OUTPUT_PATH = os.path.join("data", "processed", "ceas_sample_200.csv")


def build_sample():
    df = pd.read_csv(RAW_PATH)

    df = df[["sender", "subject", "body", "label", "urls"]].copy()

    df = df.dropna(subset=["body", "label"])

    phishing = df[df["label"] == 1].sample(
        n=100,
        random_state=42
    )

    legitimate = df[df["label"] == 0].sample(
        n=100,
        random_state=42
    )

    sample = pd.concat([phishing, legitimate])

    sample = sample.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    sample.insert(0, "source", "CEAS_08")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    sample.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print("Saved:", OUTPUT_PATH)
    print("Rows:", len(sample))
    print(sample["label"].value_counts())


if __name__ == "__main__":
    build_sample()