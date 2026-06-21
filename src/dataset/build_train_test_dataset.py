import os
import pandas as pd
from sklearn.model_selection import train_test_split


RAW_FILES = {
    "CEAS_08": r"..\archive\CEAS_08.csv",
    "SpamAssasin": r"..\archive\SpamAssasin.csv",
    "Nazario": r"..\archive\Nazario.csv",
}

OUTPUT_TRAIN = os.path.join("data", "processed", "train_dataset.csv")
OUTPUT_TEST = os.path.join("data", "processed", "test_dataset.csv")


def load_and_standardize(source_name, file_path):
    df = pd.read_csv(file_path)

    df = df[["sender", "subject", "body", "label", "urls"]].copy()

    df = df.dropna(subset=["body", "label"])

    df["source"] = source_name

    df["label"] = df["label"].astype(int)

    return df[["source", "sender", "subject", "body", "urls", "label"]]


def split_dataset(df):
    if df["label"].nunique() > 1:
        train, test = train_test_split(
            df,
            test_size=0.30,
            random_state=42,
            stratify=df["label"],
        )
    else:
        train, test = train_test_split(
            df,
            test_size=0.30,
            random_state=42,
        )

    return train, test


def build_train_test():
    train_parts = []
    test_parts = []

    for source_name, file_path in RAW_FILES.items():
        print(f"\nProcessing {source_name}...")

        df = load_and_standardize(source_name, file_path)

        print("Rows:", len(df))
        print("Label counts:")
        print(df["label"].value_counts())

        train, test = split_dataset(df)

        train_parts.append(train)
        test_parts.append(test)

        print("Train:", len(train))
        print("Test:", len(test))

    train_dataset = pd.concat(train_parts).sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    test_dataset = pd.concat(test_parts).sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    os.makedirs("data/processed", exist_ok=True)

    train_dataset.to_csv(
        OUTPUT_TRAIN,
        index=False,
        encoding="utf-8"
    )

    test_dataset.to_csv(
        OUTPUT_TEST,
        index=False,
        encoding="utf-8"
    )

    print("\nSaved train dataset:", OUTPUT_TRAIN)
    print("Train rows:", len(train_dataset))
    print(train_dataset["label"].value_counts())

    print("\nSaved test dataset:", OUTPUT_TEST)
    print("Test rows:", len(test_dataset))
    print(test_dataset["label"].value_counts())


if __name__ == "__main__":
    build_train_test()