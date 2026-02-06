import json
from pathlib import Path
from datetime import datetime
from typing import Dict

AUDIT_DIR = Path(__file__).parent.parent / "data" / "audit_logs"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def write_audit_log(doc_id: str, user_id: str, action: str, payload: Dict):
    log_entry = {
        "doc_id": doc_id,
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload
    }
    path = AUDIT_DIR / f"{doc_id}.log.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
