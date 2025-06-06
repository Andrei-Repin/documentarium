import re
from typing import List, Tuple

def format_text_to_table(text: str) -> List[Tuple[str, str, str]]:
    pattern = re.compile(r'^(\d+)\.\s*(.+?)\s+(\d{4}(?:[-–]\d{4})?)$', re.MULTILINE)
    return [(m.group(1), m.group(2).strip(), m.group(3)) for m in pattern.finditer(text)]

def format_as_tsv(rows: List[Tuple[str, str, str]]) -> str:
    return '\n'.join('\t'.join(row) for row in rows)
