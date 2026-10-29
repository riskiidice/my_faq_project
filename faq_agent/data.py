import csv
from pathlib import Path

FAQ_FIELDS = ("id", "topic", "question", "answer")

EVALUATION_FIELDS = (
    "question_id", "question", "gold_faq_id", "expected_answer", "answerable"
)


def _read_rows(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != fields:
            raise ValueError(
                f"{path} must have exactly these columns: {', '.join(fields)}")
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(
                    f"{path} row {line_number} does not match its columns")
            rows.append(row)
        return rows

def load_faqs(path: Path) -> list[dict[str, str]]:
    rows = _read_rows(path, FAQ_FIELDS)
    if not rows:
        raise ValueError(f"{path} must contain at least one FAQ")
    seen_ids = set()
    for row in rows:
        if any(not row[field] or not row[field].strip() for field in FAQ_FIELDS):
            raise ValueError(f"{path} has a blank FAQ field")
        row["id"] = row["id"].strip()
        normalized_id = row["id"].casefold()
        if normalized_id in seen_ids:
            raise ValueError(f"{path} has duplicate FAQ id {row['id']}")
        seen_ids.add(normalized_id)
    return rows


def faq_card(record: dict[str, str]) -> str:
    lines = [
        f"{record['id']} - {record['topic']}",
        f"Question: {record['question']}",
        f"Answer: {record['answer']}"
    ]
    return "\n".join(lines)
