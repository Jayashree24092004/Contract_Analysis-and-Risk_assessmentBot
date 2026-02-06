import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ExtractedEntity:
    label: str
    text: str
    start_char: int
    end_char: int

MONEY_RE = re.compile(r"(INR|Rs\.?|₹)\s?\d[\d,]*(\.\d+)?", re.IGNORECASE)
JURISDICTION_HINTS = ["courts at", "jurisdiction", "governed by", "arbitration seated in"]

def run_ner(doc, lang: str) -> List[ExtractedEntity]:
    entities = []
    for ent in doc.ents:
        entities.append(ExtractedEntity(ent.label_, ent.text, ent.start_char, ent.end_char))
    # money via regex
    for m in MONEY_RE.finditer(doc.text):
        entities.append(ExtractedEntity("MONEY_INR", m.group(0), m.start(), m.end()))
    return entities

def extract_dimensions(doc) -> Dict:
    text = doc.text.lower()
    output = {
        "parties": [],
        "amounts": [],
        "dates": [],
        "jurisdiction": [],
        "governing_law": [],
        "ip_rights": [],
        "confidentiality": [],
    }
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PERSON"):
            output["parties"].append(ent.text)
        if ent.label_ in ("DATE",):
            output["dates"].append(ent.text)
        if ent.label_ in ("MONEY",):
            output["amounts"].append(ent.text)
    for m in MONEY_RE.finditer(doc.text):
        output["amounts"].append(m.group(0))

    for clue in JURISDICTION_HINTS:
        if clue in text:
            output["jurisdiction"].append(clue)

    if "laws of india" in text or "laws of the republic of india" in text:
        output["governing_law"].append("India")

    if "intellectual property" in text or "ip" in text:
        output["ip_rights"].append("IP clause present")
    if "confidential" in text or "non-disclosure" in text:
        output["confidentiality"].append("Confidentiality/NDA clause present")
    return output
from typing import List, Dict

OBLIGATION_WORDS = ["shall", "must", "is obliged to", "is required to", "has to"]
RIGHT_WORDS = ["may", "is entitled to", "reserves the right to"]
PROHIBITION_WORDS = ["shall not", "must not", "is prohibited from", "no party shall"]

def classify_sentence_role(sent: str) -> str:
    s_lower = sent.lower()
    if any(p in s_lower for p in PROHIBITION_WORDS):
        return "prohibition"
    if any(o in s_lower for o in OBLIGATION_WORDS):
        return "obligation"
    if any(r in s_lower for r in RIGHT_WORDS):
        return "right"
    return "neutral"

def classify_clause_roles(doc) -> List[Dict]:
    roles = []
    for sent in doc.sents:
        role = classify_sentence_role(sent.text)
        if role != "neutral":
            roles.append({"sentence": sent.text, "role": role})
    return roles
