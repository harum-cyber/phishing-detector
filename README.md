# Hybrid Phishing Detection System

A hybrid phishing email detection framework that combines **Protocol Validation** with **Large Language Model (LLM) Semantic Analysis** to detect modern phishing attacks, including template-based and AI-generated phishing emails.

---

## Overview

Traditional phishing detection systems often rely on handcrafted rules or machine learning models that struggle with modern phishing emails generated using Large Language Models.

This project proposes a hybrid framework that combines:

- Protocol Validation
- LLM Semantic Analysis
- Hybrid Risk Fusion Engine

to produce a robust, explainable phishing detection system.

---

## Features

- Email (.eml) parsing
- HTML cleaning
- URL extraction
- Sender analysis
- URL validation
- Domain mismatch detection
- LLM semantic analysis (OpenRouter + Llama 3.1)
- Risk Fusion Engine
- Explainable phishing classification
- Streamlit graphical interface
- FastAPI backend

---

## System Architecture

The proposed framework consists of three major layers:

1. Protocol Validation Layer
2. LLM Semantic Analysis Layer
3. Hybrid Fusion Engine

These components work together to produce the final phishing classification.

---

## Dataset

Public phishing email datasets were used:

- CEAS_08
- SpamAssassin
- Nazario

Final processed dataset:

- 46,527 emails

Evaluation set:

- 13,960 emails

---

## Technologies

- Python
- Streamlit
- FastAPI
- OpenRouter API
- Llama 3.1
- Pandas

---

## Performance

| Metric | Value |
|--------|-------|
| Accuracy | 85.23% |
| Precision | 92.17% |
| Recall | 79.38% |
| F1-score | 85.30% |

---

## User Interface

The application allows users to upload an `.eml` file and automatically performs:

- Protocol Validation
- Semantic Analysis
- Hybrid Risk Fusion

The interface provides:

- Final classification
- Risk level
- Risk score
- Protocol findings
- Semantic indicators
- Decision explanation
- Recommended action

---

## Research

This implementation was developed as part of the MSc dissertation:

**A Robust Phishing Detection Method Against Template-based Attacks Using Large Language Model Semantic Analysis and Protocol Validation**

University of Gezira
Faculty of Mathematical and Computer Sciences

2026

---

## Future Work

Future improvements include:

- Protocol-aware prompting
- Fine-tuning using phishing-specific datasets
- Local LLM deployment
- Enterprise email evaluation
- Multilingual phishing detection
- Retrieval-Augmented Generation (RAG)

---

## License

This repository is intended for academic and research purposes.
