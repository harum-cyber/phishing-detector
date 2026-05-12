import os

from src.evaluation.batch_evaluator import BatchEvaluator


phishing_folder = os.path.join("data", "raw", "phishing")
legitimate_folder = os.path.join("data", "raw", "legitimate")

phishing_results = BatchEvaluator.evaluate(phishing_folder, True)
legitimate_results = BatchEvaluator.evaluate(legitimate_folder, False)

all_results = phishing_results + legitimate_results

print("\n=== Batch Evaluation Results ===\n")

for result in all_results:
    print(result)

correct_count = sum(1 for result in all_results if result["correct"])
total_count = len(all_results)

accuracy = correct_count / total_count if total_count > 0 else 0

print("\nAccuracy:")
print(accuracy)