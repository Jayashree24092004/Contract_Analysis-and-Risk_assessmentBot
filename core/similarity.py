from pathlib import Path
from typing import Dict, Tuple
import spacy

from . import NLP_EN

TEMPLATE_DIR = Path(__file__).parent.parent / "config" / "templates"


def load_template_clauses(contract_type: str) -> Dict[str, str]:
    path = TEMPLATE_DIR / f"{contract_type}_en.txt"

    # ✅ FIX 1: Handle missing template file safely
    if not path.exists():
        return {}

    text_data = path.read_text(encoding="utf-8").strip()
    if not text_data:
        return {}

    blocks = text_data.split("\n\n")
    out = {}
    name = None
    text = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        if block.startswith("[") and block.endswith("]"):
            if name:
                out[name] = "\n".join(text).strip()
                text = []
            name = block.strip("[]")
        else:
            text.append(block)

    if name and text:
        out[name] = "\n".join(text).strip()

    return out


def best_template_match(
    clause_text: str,
    contract_type: str,
    nlp=None
) -> Tuple[str, float]:

    # ✅ FIX 2: Guard bad clause text
    if not clause_text or not isinstance(clause_text, str):
        return "", 0.0

    nlp = nlp or NLP_EN

    templates = load_template_clauses(contract_type)
    if not templates:
        return "", 0.0

    try:
        doc_c = nlp(clause_text)
    except Exception:
        return "", 0.0

    best_name, best_score = "", 0.0

    for name, tmpl in templates.items():
        if not tmpl:
            continue
        try:
            doc_t = nlp(tmpl)
            score = doc_c.similarity(doc_t)
        except Exception:
            continue

        if score > best_score:
            best_score, best_name = score, name

    return best_name, best_score
