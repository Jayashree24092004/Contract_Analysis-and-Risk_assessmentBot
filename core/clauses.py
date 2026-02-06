import re
from dataclasses import dataclass, field
from typing import List, Optional

CLAUSE_HEADING_RE = re.compile(
    r"(^\d+(\.\d+)*\s+.+|^clause\s+\d+.+|^section\s+\d+.+)",
    re.IGNORECASE | re.MULTILINE,
)

@dataclass
class Clause:
    id: str
    heading: str
    text: str
    subclauses: List["Clause"] = field(default_factory=list)

def split_into_clauses(text: str) -> List[Clause]:
    matches = list(CLAUSE_HEADING_RE.finditer(text))
    clauses: List[Clause] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = m.group(0).strip()
        body = text[start:end].strip()
        clauses.append(Clause(id=f"C{i+1}", heading=heading, text=body))
    if not clauses:
        clauses.append(Clause(id="C1", heading="Entire Agreement", text=text))
    return clauses
