import os
import tempfile
import streamlit as st

from main import run_pipeline


st.set_page_config(
    page_title="Hybrid Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Hybrid Phishing Detection System")
st.write("LLM Semantic Analysis + Protocol Validation + Hybrid Fusion Engine")

uploaded_file = st.file_uploader(
    "Upload an email file (.eml)",
    type=["eml"]
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        with st.spinner("Analyzing email..."):
            result = run_pipeline(temp_path)

        decision = result["decision"]

        st.subheader("Final Decision")

        col1, col2, col3 = st.columns(3)

        col1.metric("Prediction", "Phishing" if decision["is_phishing"] else "Legitimate")
        col2.metric("Risk Level", decision["risk"].upper())
        col3.metric("Score", decision["score"])

        if decision["is_phishing"]:
            st.error("This email is classified as phishing.")
        else:
            st.success("This email is classified as legitimate.")

        st.subheader("Email Summary")
        st.write("**Subject:**", result["email"]["subject"])
        st.write("**Sender:**", result["email"]["sender"])
        st.write("**Semantic Source:**", result["semantic_source"])

        st.subheader("Reasons")
        for reason in decision["reasons"]:
            st.write("-", reason)

        if decision.get("recommended_action"):
            st.subheader("Recommended Action")
            st.info(decision["recommended_action"])

        st.subheader("Protocol Analysis")
        st.json(result["protocol"])

        st.subheader("LLM Semantic Analysis")
        st.json(result["semantic"])

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)