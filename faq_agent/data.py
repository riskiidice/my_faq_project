import csv
from pathlib import Path

FAQ_FIELDS = ("id", "topic", "question", "answer")


def load_faqs(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != FAQ_FIELDS:
            raise ValueError(
                f"{path} must have exactly these columns : {", ".join(FAQ_FIELDS)}")
        rows = list(reader)
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
