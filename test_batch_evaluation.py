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

tp = 0
tn = 0
fp = 0
fn = 0

for result in all_results:

    predicted = result["predicted"]
    expected = result["expected"]

    if predicted and expected:
        tp += 1

    elif not predicted and not expected:
        tn += 1

    elif predicted and not expected:
        fp += 1

    elif not predicted and expected:
        fn += 1


accuracy = (tp + tn) / len(all_results)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0

recall = tp / (tp + fn) if (tp + fn) > 0 else 0

f1_score = (
    2 * precision * recall / (precision + recall)
    if (precision + recall) > 0
    else 0
)

print("\n=== Metrics ===\n")

print("TP:", tp)
print("TN:", tn)
print("FP:", fp)
print("FN:", fn)

print("\nAccuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1_score)