\# Hybrid Phishing Detection System Design



\## Overview



This project implements a hybrid phishing email detection framework that combines:



1\. Semantic Similarity Analysis

2\. Protocol Validation

3\. Hybrid Decision Engine



The goal is to improve robustness against template-based phishing and GenAI-generated phishing attacks.



---



\# System Architecture



The system processes phishing emails through multiple stages:



.eml Email

&nbsp;   ↓

Email Parser

&nbsp;   ↓

HTML Cleaner

&nbsp;   ↓

+----------------------+

| Semantic Layer       |

| - Social engineering |

| - Urgency detection  |

| - Credential cues    |

+----------------------+

&nbsp;   ↓

+----------------------+

| Protocol Layer       |

| - URL Analysis       |

| - Sender Analysis    |

| - Domain Validation  |

+----------------------+

&nbsp;   ↓

Hybrid Decision Engine

&nbsp;   ↓

Final Risk Classification



---



\# Components



\## 1. Email Parser



Responsible for:

\- Reading .eml email files

\- Extracting:

&nbsp; - Subject

&nbsp; - Sender

&nbsp; - Body



File:

\- src/preprocessing/email\_parser.py



---



\## 2. HTML Cleaner



Responsible for:

\- Parsing HTML emails

\- Extracting hyperlinks

\- Cleaning raw HTML text



File:

\- src/preprocessing/html\_cleaner.py



---



\## 3. URL Analyzer



Responsible for:

\- Extracting URL components

\- Detecting suspicious URL indicators:

&nbsp; - HTTP usage

&nbsp; - Hyphenated domains

&nbsp; - Long domains



File:

\- src/protocol\_layer/url\_analyzer.py



---



\## 4. Sender Analyzer



Responsible for:

\- Extracting sender email/domain

\- Detecting suspicious sender behavior



File:

\- src/protocol\_layer/sender\_analyzer.py



---



\## 5. Semantic Analyzer



Current Version:

\- Rule-based semantic detector



Detects:

\- Urgency language

\- Threat language

\- Credential-related language



Future Version:

\- LLM-powered semantic reasoning



File:

\- src/semantic\_layer/semantic\_analyzer.py



---



\## 6. Hybrid Decision Engine



Responsible for:

\- Combining:

&nbsp; - Semantic analysis

&nbsp; - Protocol validation

\- Generating:

&nbsp; - Final phishing classification

&nbsp; - Risk level

&nbsp; - Explanations



File:

\- src/decision\_engine/rule\_based\_decision.py



---



\# Current Features



Implemented:

\- Email parsing

\- HTML cleaning

\- URL extraction

\- URL analysis

\- Sender analysis

\- Domain mismatch detection

\- Semantic analysis

\- Hybrid decision logic



---



\# Future Work



Planned improvements:

\- Real LLM integration

\- Threat intelligence APIs

\- Batch evaluation

\- Accuracy metrics

\- Adversarial robustness testing

\- Explainable AI outputs

\- Prompt engineering optimization



