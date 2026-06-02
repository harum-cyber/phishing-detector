import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException

from main import run_pipeline


app = FastAPI(
    title="Hybrid Phishing Detection API",
    description="LLM-ready hybrid phishing detection system using semantic and protocol validation.",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze-email")
async def analyze_email(file: UploadFile = File(...)):
    if not file.filename.endswith(".eml"):
        raise HTTPException(status_code=400, detail="Only .eml files are supported")

    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        result = run_pipeline(temp_path)
        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)