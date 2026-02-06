from enum import Enum

class ContractType(str, Enum):
    EMPLOYMENT = "employment"
    VENDOR = "vendor"
    LEASE = "lease"
    PARTNERSHIP = "partnership"
    SERVICE = "service"
    OTHER = "other"

KEYWORDS = {
    ContractType.EMPLOYMENT: ["employee", "employer", "salary", "employment"],
    ContractType.VENDOR: ["supplier", "purchase order", "vendor", "supply"],
    ContractType.LEASE: ["lease", "tenant", "landlord", "rent"],
    ContractType.PARTNERSHIP: ["partners", "partnership", "profit sharing"],
    ContractType.SERVICE: ["services", "service provider", "SLA", "performance"],
}

def rule_based_contract_type(text: str) -> ContractType:
    t = text.lower()
    scores = {ct: 0 for ct in KEYWORDS}
    for ct, words in KEYWORDS.items():
        scores[ct] = sum(1 for w in words if w in t)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else ContractType.OTHER

def classify_contract(text: str, llm_client) -> ContractType:
    ct = rule_based_contract_type(text)
    if ct != ContractType.OTHER:
        return ct
    # LLM refinement
    label = llm_client.classify_contract_type(text)
    try:
        return ContractType(label)
    except ValueError:
        return ContractType.OTHER
