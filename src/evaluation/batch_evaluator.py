import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import run_pipeline


class BatchEvaluator:

    @staticmethod
    def evaluate(folder_path, expected_label):

        results = []

        for filename in os.listdir(folder_path):

            if filename.endswith(".eml"):

                file_path = os.path.join(folder_path, filename)

                result = run_pipeline(file_path)

                predicted = result["decision"]["is_phishing"]

                correct = (predicted == expected_label)

                results.append({
                    "file": filename,
                    "predicted": predicted,
                    "expected": expected_label,
                    "correct": correct,
                    "risk": result["decision"]["risk"]
                })

        return results