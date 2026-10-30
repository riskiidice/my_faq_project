import json
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


def load_evaluation(path: Path) -> list[dict[str, str | bool]]:
    rows = _read_rows(path, EVALUATION_FIELDS)
    result = []
    seen_ids = set()
    for row in rows:
        row = {field: value.strip() for field, value in row.items()}
        if not row["question_id"] or not row["question"]:
            raise ValueError(f"{path} has a blank question id or question")
        if row["question_id"] in seen_ids:
            raise ValueError(
                f"{path} has duplicate question id {row['question_id']}")
        if row["answerable"] not in ("true", "false"):
            raise ValueError(f"{path} answerable values must be true or false")
        answerable = row["answerable"] == "true"
        has_gold = bool(row["gold_faq_id"])
        has_expected = bool(row["expected_answer"])
        if answerable and not (has_gold and has_expected):
            raise ValueError(
                f"{path} answerable rows need a gold ID and expected answer")
        if not answerable and (has_gold or has_expected):
            raise ValueError(
                f"{path} answerability does not match its gold fields")
        seen_ids.add(row["question_id"])
        result.append({**row, "answerable": answerable})
    return result


def load_questions(path: Path) -> list[dict]:
    required = {
        "question_id", "type", "level", "question", "gold_cards",
        "gold_answers", "answerable", "split",
    }
    questions = []
    seen_ids = set()
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{path} line {line_number} is not valid JSON") from error
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError(f"{path} line {line_number} has the wrong fields")
        text_fields = ("question_id", "type", "level", "question", "split")
        if not all(isinstance(row[key], str) and row[key] for key in text_fields):
            raise ValueError(
                f"{path} line {line_number} has a blank text field")
        if row["question_id"] in seen_ids:
            raise ValueError(
                f"{path} has duplicate question id {row['question_id']}")
        if row["level"] not in {"basic", "hard"}:
            raise ValueError(f"{path} line {line_number} has an invalid level")
        if row["split"] not in {"tuning", "heldout"}:
            raise ValueError(f"{path} line {line_number} has an invalid split")
        if not isinstance(row["gold_cards"], list) or not all(
            isinstance(value, str) for value in row["gold_cards"]
        ):
            raise ValueError(
                f"{path} line {line_number} has invalid gold_cards")
        if not isinstance(row["gold_answers"], list) or not all(
            isinstance(value, str) for value in row["gold_answers"]
        ):
            raise ValueError(
                f"{path} line {line_number} has invalid gold_answers")
        if not isinstance(row["answerable"], bool):
            raise ValueError(
                f"{path} line {line_number} has invalid answerable")
        if row["answerable"] != bool(row["gold_cards"]):
            raise ValueError(
                f"{path} line {line_number} has inconsistent answerability")
        seen_ids.add(row["question_id"])
        questions.append(row)
    return questions
