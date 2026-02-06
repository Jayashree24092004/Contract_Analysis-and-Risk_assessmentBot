import json
from pathlib import Path
from collections import Counter

KB_PATH = Path(__file__).parent.parent / "data" / "kb" / "kb.json"

def update_kb_from_analysis(analysis: dict):
    KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if KB_PATH.exists():
        kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    else:
        kb = {"issue_counts": {}, "examples": {}}

    counts = Counter(kb["issue_counts"])
    for clause in analysis["clauses"]:
        for flag, val in clause["risk"]["flags"].items():
            if val:
                counts[flag] += 1
                kb["examples"].setdefault(flag, []).append({
                    "doc_id": analysis["doc_id"],
                    "clause_id": clause["id"],
                    "snippet": clause["text"][:250]
                })

    kb["issue_counts"] = dict(counts)
    KB_PATH.write_text(json.dumps(kb, indent=2), encoding="utf-8")
