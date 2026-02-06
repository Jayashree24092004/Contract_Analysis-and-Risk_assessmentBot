#  GenAI-Powered Legal Contract Assistant for Indian SMEs

## 🔗 Live Demo
https://jdzdq814-8504.inc1.devtunnels.ms/

---

## 📌 Problem Statement

Small and Medium Enterprises (SMEs) in India frequently deal with complex legal contracts such as employment agreements, vendor contracts, lease agreements, and service contracts. These documents often contain hidden legal risks that are difficult to understand without legal expertise.

This project builds a **GenAI-powered legal assistant** that helps SMEs:
- Understand contracts in simple language
- Identify risky clauses
- Receive actionable suggestions
- Support English and Hindi contracts

---

## 🎯 Key Features

### Core Legal NLP Tasks
- Contract type classification
- Clause and sub-clause extraction
- Named Entity Recognition (parties, dates, jurisdiction, amounts)
- Obligation vs right vs prohibition identification
- Ambiguity detection
- Clause similarity matching to standard templates

### Risk Assessment
- Clause-level risk scoring (Low / Medium / High)
- Contract-level composite risk score
- Detection of:
  - Penalty clauses
  - Indemnity clauses
  - Unilateral termination
  - Auto-renewal and lock-in periods
  - Non-compete and IP transfer clauses

### User-Facing Outputs
- Simplified contract summary
- Clause-by-clause AI insights (ChatGPT-like)
- Plain-language explanations
- Suggested renegotiation alternatives
- Risk visualization (charts)
- PDF and JSON export
- Audit logging

---

## 🌐 Multilingual Support
- English and Hindi contract parsing
- Hindi → English internal normalization for NLP
- Output explanations available in English or Hindi

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|------------|
| UI | Streamlit |
| LLM | GPT-4 / Claude-3 (fallback demo mode supported) |
| NLP | spaCy (English & Hindi pipelines) |
| Risk Engine | Rule-based Python engine |
| Visualization | Plotly |
| Storage | Local files + JSON |
| Export | PDF / JSON |

⚠️ No external legal APIs or case law databases are used.

---
## 📁 Project Folder Structure

```text
hcl_hackathon/
│
├── app_streamlit.py
│   └── Main Streamlit application
│       • UI rendering
│       • File upload
│       • Language selection (English / Hindi)
│       • Clause-level AI insights
│       • Risk visualization (Plotly)
│       • PDF / JSON export
│
├── core/
│   ├── ingest.py
│   │   └── Handles document ingestion
│   │       • PDF / DOCX / TXT text extraction
│   │
│   ├── preprocess.py
│   │   └── Text preprocessing
│   │       • Language detection
│   │       • Cleaning
│   │       • Hindi → English normalization
│   │
│   ├── classify.py
│   │   └── Contract type classification
│   │       • Employment
│   │       • Vendor
│   │       • Lease
│   │       • Partnership
│   │       • Service
│   │
│   ├── clauses.py
│   │   └── Clause & sub-clause extraction logic
│   │
│   ├── ner_obligations.py
│   │   └── NLP-based extraction
│   │       • Parties
│   │       • Dates
│   │       • Jurisdiction
│   │       • Obligations vs Rights vs Prohibitions
│   │
│   ├── risk_engine.py
│   │   └── Rule-based risk scoring engine
│   │       • Clause-level risk (Low / Medium / High)
│   │       • Contract-level composite risk
│   │       • Penalty, indemnity, lock-in, IP risks
│   │
│   ├── ambiguity.py
│   │   └── Detects ambiguous legal language
│   │       • e.g., “best efforts”, “reasonable time”
│   │
│   ├── similarity.py
│   │   └── Clause similarity matching
│   │       • Compares clauses with SME-friendly templates
│   │
│   ├── llm_client.py
│   │   └── GenAI interaction layer
│   │       • ChatGPT-like AI insights
│   │       • Clause explanation
│   │       • Alternative clause suggestions
│   │       • Multilingual support (English / Hindi)
│   │
│   ├── reports.py
│   │   └── Report generation
│   │       • JSON output
│   │       • PDF export for legal review
│   │
│   ├── audit.py
│   │   └── Audit logging
│   │       • Upload tracking
│   │       • Analysis history
│   │
│   └── kb.py
│       └── Knowledge base updates
│           • Stores common SME contract issues
│
├── config/
│   └── templates/
│       └── Standard SME-friendly clause templates
│
├── data/
│   ├── uploads/
│   │   └── User-uploaded contracts
│   │
│   └── outputs/
│       └── Generated reports (PDF / JSON)
│
├── venv/
│   └── Python virtual environment (local use)
│
├── requirements.txt
│   └── Project dependencies
│
└── README.md
    └── Project documentation

---

### 🧩 System Flow

1. User uploads contract (PDF/DOCX/TXT)
2. Text extraction and language detection
3. Hindi → English normalization (if needed)
4. Clause segmentation
5. NLP-based entity extraction
6. Risk and compliance detection
7. AI-generated insights and explanations
8. Risk visualization
9. Export reports and audit logs

---

### 📊 Visualization Example
- Clause risk distribution using interactive pie charts
- Helps SMEs understand contract risk at a glance

---

### 📁 Project Structure
### <img width="1916" he<img width="1912" height="637" alt="image" src="https://github.com/user-attachments/assets/e783c7d8-1e49-4dcb-ad4a-a312726fa2d4" />
### <img width="1912" height="637" alt="image" src="https://github.com/user-attachments/assets/463c7cb4-2f8c-4e26-8a69-801e96909513" />



