from main import run_pipeline
import time

for i in range(20):
    result = run_pipeline(
        "data/raw/sample_phishing.eml"
    )

    print(
        f"{i+1}:",
        result["decision"]["risk"]
    )

    time.sleep(1)