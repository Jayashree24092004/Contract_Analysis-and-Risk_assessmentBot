import json
import re
from pathlib import Path
from typing import List, Dict

# Load risk configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "risk_config.json"
if CONFIG_PATH.exists():
    CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
else:
    # Fallback defaults if config file missing
    CONFIG = {
        "risk_weights": {
            "penalty_clause": 3,
            "broad_indemnity": 4,
            "unilateral_termination": 4,
            "auto_renewal": 2,
            "long_lock_in": 3,
            "broad_non_compete": 4,
            "full_ip_transfer": 3,
            "missing_dispute_resolution": 2
        },
        "thresholds": {"low": 0, "medium": 6, "high": 12},
        "lock_in_max_months": 12
    }


def has_penalty_clause(text: str) -> bool:
    t = text.lower()
    return "penalty" in t or "liquidated damages" in t


def has_unilateral_termination(text: str) -> bool:
    t = text.lower()
    return ("company may terminate" in t and "employee may terminate" not in t) or \
           ("client may terminate" in t and "service provider may terminate" not in t)


def has_auto_renewal(text: str) -> bool:
    t = text.lower()
    return "auto-renew" in t or "automatically renew" in t or "shall renew" in t


def has_long_lockin(text: str, max_months: int) -> bool:
    m = re.search(r"lock[- ]?in.*?(\d+)\s*(months|month)", text.lower())
    if not m:
        return False
    months = int(m.group(1))
    return months > max_months


def has_broad_non_compete(text: str) -> bool:
    t = text.lower()
    return "non-compete" in t or "non compete" in t or "shall not engage in any competing business" in t


def has_full_ip_transfer(text: str) -> bool:
    t = text.lower()
    return "all intellectual property" in t and "assigns" in t


def detect_risk_flags(clause_text: str) -> Dict[str, bool]:
    return {
        "penalty_clause": has_penalty_clause(clause_text),
        "unilateral_termination": has_unilateral_termination(clause_text),
        "auto_renewal": has_auto_renewal(clause_text),
        "long_lock_in": has_long_lockin(clause_text, CONFIG["lock_in_max_months"]),
        "broad_non_compete": has_broad_non_compete(clause_text),
        "full_ip_transfer": has_full_ip_transfer(clause_text),
    }


def score_clause(clause_text: str) -> Dict:
    flags = detect_risk_flags(clause_text)
    score = 0
    contributions: Dict[str, int] = {}
    for key, value in flags.items():
        if value:
            w = CONFIG["risk_weights"].get(key, 0)
            score += w
            contributions[key] = w

    thr = CONFIG["thresholds"]
    if score >= thr["high"]:
        level = "high"
    elif score >= thr["medium"]:
        level = "medium"
    else:
        level = "low"

    return {"score": score, "level": level, "flags": flags, "contributions": contributions}


def score_contract(clauses: List) -> Dict:
    """
    clauses: list of Clause objects with .text attribute.
    """
    clause_scores = [score_clause(c.text) for c in clauses]
    total = sum(c["score"] for c in clause_scores)
    avg = total / max(len(clause_scores), 1)

    thr = CONFIG["thresholds"]
    if avg >= thr["high"]:
        level = "high"
    elif avg >= thr["medium"]:
        level = "medium"
    else:
        level = "low"

    return {
        "total_score": total,
        "avg_score": avg,
        "level": level,
        "clause_scores": clause_scores,
    }
