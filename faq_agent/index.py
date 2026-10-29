import json
from faq_agent.data import faq_card
from pathlib import Path


def faq_rows(records: list[dict]) -> list[dict]:
    return [
        {
            "id": record["id"],
            "topic": record["topic"],
            "question": record["question"],
            "answer": record["answer"],
            "text": faq_card(record),
        }
        for record in records
    ]


def save_rows(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
