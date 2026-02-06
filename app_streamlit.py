import streamlit as st
from pathlib import Path
from uuid import uuid4

from core.ingest import load_document
from core.preprocess import detect_language, clean_text, normalize_for_nlp
from core import NLP_EN, NLP_HI
from core.classify import classify_contract
from core.clauses import split_into_clauses
from core.ner_obligations import extract_dimensions, classify_clause_roles
from core.risk_engine import score_contract, score_clause
from core.ambiguity import clause_ambiguity_annotations
from core.similarity import best_template_match
from core.llm_client import LLMClient
from core.reports import gen_json_report, gen_pdf_report
from core.audit import write_audit_log
from core.kb import update_kb_from_analysis

output_lang = st.selectbox(
    "Explanation language",
    ["English", "Hindi"]
)

# ------------------ Helpers ------------------
def generate_ai_insight_llm(
    clause_text: str,
    clause_risk: dict,
    output_lang: str,
    llm_client
):
    level = clause_risk.get("level", "low")
    flags = clause_risk.get("flags", [])

    language_instruction = (
        "Respond in simple Hindi (Devanagari script)."
        if output_lang == "Hindi"
        else "Respond in simple business English."
    )

    prompt = f"""
You are a legal AI assistant for Indian SME contracts.

Analyze the following contract clause and provide an AI insight.
Explain:
• Whether the clause is safe, acceptable, or risky
• Why it matters for a small business
• What could be improved (if needed)

Clause:
\"\"\"{clause_text}\"\"\"

Risk level: {level}
Risk flags: {", ".join(flags) if flags else "None"}

{language_instruction}
"""

    try:
        return llm_client.chat(prompt)
    except Exception:
        if level == "low":
            return (
                "यह क्लॉज संतुलित और व्यवसाय के लिए सुरक्षित है।"
                if output_lang == "Hindi"
                else "This clause is balanced and generally safe for the business."
            )
        elif level == "medium":
            return (
                "यह क्लॉज कुछ जोखिम पैदा कर सकता है और सावधानी की आवश्यकता है।"
                if output_lang == "Hindi"
                else "This clause carries some risk and should be reviewed carefully."
            )
        else:
            return (
                "यह क्लॉज उच्च जोखिम वाला है और पुनः बातचीत की आवश्यकता है।"
                if output_lang == "Hindi"
                else "This clause is high risk and should be renegotiated."
            )

# ------------------ Setup ------------------

UPLOAD_DIR = Path("data/uploads")
OUTPUT_DIR = Path("data/outputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

llm_client = LLMClient(provider="gpt4", api_key="YOUR_KEY")

st.title("SME GenAI Contract Assistant (India)")
user_id = "local_user"

uploaded = st.file_uploader(
    "Upload contract (PDF / DOCX / TXT)",
    type=["pdf", "doc", "docx", "txt"]
)

if uploaded is None:
    st.info("Please upload a contract to begin analysis.")
    st.stop()


# ------------------ Ingestion ------------------

doc_id = str(uuid4())
file_path = UPLOAD_DIR / f"{doc_id}_{uploaded.name}"

with open(file_path, "wb") as f:
    f.write(uploaded.getbuffer())

write_audit_log(doc_id, user_id, "upload", {"filename": uploaded.name})

raw_text = load_document(file_path)
if not raw_text or not isinstance(raw_text, str):
    st.error("Failed to extract text from the uploaded document.")
    st.stop()

text_clean = clean_text(raw_text)
if not text_clean.strip():
    st.error("Document appears empty after cleaning.")
    st.stop()

lang = detect_language(text_clean)
force_hi = st.checkbox("Treat as Hindi contract (force Hindi → English)")

norm_text = text_clean
processing_lang = lang

if force_hi or lang == "hi":
    norm_text = normalize_for_nlp(text_clean, "hi", llm_client)
    if not norm_text or not isinstance(norm_text, str):
        st.error("Hindi normalization failed.")
        st.stop()
    nlp = NLP_EN
    processing_lang = "en"
else:
    nlp = NLP_EN if lang == "en" else NLP_HI

doc = nlp(norm_text)
def translate_if_needed(text: str, target_lang: str, llm_client):
    if not text or target_lang != "Hindi":
        return text
    try:
        return llm_client.translate_text(
            text=text,
            target_language="hi"
        )
    except Exception:
        return text



# ------------------ Analysis ------------------

ctype = classify_contract(norm_text, llm_client)

clauses = split_into_clauses(norm_text)
risk_contract = score_contract(clauses)
ambiguity_ann = clause_ambiguity_annotations(clauses)

dims = extract_dimensions(doc)
roles = classify_clause_roles(doc)

clause_results = []

for i, c in enumerate(clauses):
    c_risk = score_clause(c.text)

    ai_insight = generate_ai_insight_llm(
        clause_text=c.text,
        clause_risk=c_risk,
        output_lang=output_lang,
        llm_client=llm_client
    )

    name, sim = best_template_match(c.text, ctype.value)

    plain_en = llm_client.explain_clause(c.text, c_risk, lang="en")
    plain = translate_if_needed(plain_en, output_lang, llm_client)

    alt_clause = None
    if c_risk["level"] != "low":
        alt_clause = llm_client.suggest_alternative_clause(
            c.text,
            c_risk["flags"],
            ctype.value
        )

    clause_results.append({
        "id": c.id,
        "heading": c.heading,
        "text": c.text,
        "risk": c_risk,
        "ai_insight": ai_insight,
        "template_match": {"name": name, "similarity": sim},
        "plain_explanation": plain,
        "alternative": alt_clause,
        "ambiguous": ambiguity_ann[i]["ambiguous"]
    })




# ------------------ Contract Summary ------------------

summary_en = llm_client.summarize_contract(
    extracted_info={
        "contract_type": ctype.value,
        "dimensions": dims,
        "roles": roles
    },
    risk_summary=risk_contract,
    lang="en"
)

summary_text = translate_if_needed(summary_en, output_lang, llm_client)

analysis = {
    "doc_id": doc_id,
    "contract_type": ctype.value,
    "language_detected": processing_lang,
    "risk": risk_contract,
    "dimensions": dims,
    "summary": summary_text,
    "clauses": clause_results
}

update_kb_from_analysis(analysis)
write_audit_log(doc_id, user_id, "analysis_completed", {"risk": risk_contract})


# ------------------ Visualization ------------------

import plotly.express as px
import pandas as pd

st.subheader("📊 Clause Risk Distribution")

risk_levels = [c["risk"]["level"] for c in clause_results]
risk_df = pd.DataFrame(risk_levels, columns=["Risk"])

if output_lang == "Hindi":
    risk_df["Risk"] = risk_df["Risk"].replace({
        "low": "कम जोखिम",
        "medium": "मध्यम जोखिम",
        "high": "उच्च जोखिम"
    })

fig = px.pie(
    risk_df,
    names="Risk",
    title="Clause Risk Distribution",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)


# ------------------ UI ------------------

st.subheader("Overall Contract Risk")
st.metric(
    "Risk Level",
    risk_contract["level"],
    f"{risk_contract['avg_score']:.1f} average score"
)

st.write(summary_text)

st.subheader("Key Extracted Information")
st.json(dims)

st.subheader("Clause-level Analysis")

filter_level = st.selectbox(
    "Filter by risk level",
    ["all", "low", "medium", "high"]
)

for c in clause_results:
    if filter_level != "all" and c["risk"]["level"] != filter_level:
        continue

    with st.expander(f"{c['id']} - {c['heading']} ({c['risk']['level']})"):
        st.write("**Original Clause**")
        st.write(c["text"])

        st.write("**AI Insight**")
        st.info(c["ai_insight"])

        st.write("**Plain Explanation**")
        st.write(c["plain_explanation"])

        if c["ambiguous"]:
            st.warning("This clause contains potentially ambiguous wording.")

        if c["alternative"]:
            st.write("**Suggested Improved Clause**")
            st.write(c["alternative"])


# ------------------ Exports ------------------

st.subheader("Exports")

if st.button("Generate JSON Report"):
    json_path = gen_json_report(OUTPUT_DIR, analysis)
    with open(json_path, "rb") as f:
        st.download_button("Download JSON", f, json_path.name)

if st.button("Generate PDF Report"):
    pdf_path = gen_pdf_report(OUTPUT_DIR, analysis)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, pdf_path.name)


# ------------------ Sidebar ------------------

st.sidebar.header("Standard Contract Templates")

contract_type_for_template = st.sidebar.selectbox(
    "Generate SME-friendly template",
    ["employment", "vendor", "lease", "partnership", "service"]
)

if st.sidebar.button("Generate Template"):
    tpl = llm_client.generate_template(
        contract_type_for_template,
        {"jurisdiction": "India"}
    )
    st.sidebar.text_area("Template", tpl, height=400)
