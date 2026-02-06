AMBIGUOUS_PHRASES = [
    "best efforts", "reasonable efforts", "as soon as practicable",
    "material breach", "commercially reasonable", "from time to time"
]

def detect_ambiguity(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in AMBIGUOUS_PHRASES)

def clause_ambiguity_annotations(clauses):
    return [{"id": c.id, "ambiguous": detect_ambiguity(c.text)} for c in clauses]
