from pathlib import Path
from fpdf import FPDF
import json
from datetime import datetime

def gen_json_report(output_dir: Path, analysis: dict) -> Path:
    path = output_dir / f"report_{analysis['doc_id']}.json"
    path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    return path

def gen_pdf_report(output_dir: Path, analysis: dict) -> Path:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Contract Risk Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, f"Document ID: {analysis['doc_id']}")
    pdf.multi_cell(0, 6, f"Contract Type: {analysis['contract_type']}")
    pdf.multi_cell(0, 6, f"Overall Risk: {analysis['risk']['level']} ({analysis['risk']['avg_score']:.1f})")

    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Plain-language summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, analysis["summary"])

    for clause in analysis["clauses"]:
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 6, f"{clause['id']}: {clause['heading']}")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, clause["text"])
        pdf.ln(2)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 5, f"Risk level: {clause['risk']['level']}")
        pdf.ln(2)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, "Explanation:")
        pdf.multi_cell(0, 5, clause["plain_explanation"])
        if clause.get("alternative"):
            pdf.ln(2)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 5, "Suggested alternative:")
            pdf.multi_cell(0, 5, clause["alternative"])

    out_path = output_dir / f"report_{analysis['doc_id']}.pdf"
    pdf.output(str(out_path))
    return out_path
