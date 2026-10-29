import hashlib
import pandas as pd
import json
from pathlib import Path

from faq_agent.data import load_evaluation, load_faqs


def build_table(records: list[dict[str, str]]) -> pd.DataFrame:
    table = pd.DataFrame(records)
    return table.sort_values("id").reset_index(drop=True)


def faq_question_rows(df: pd.DataFrame) -> list[dict]:
    return [
        {
            "question_id": f"FAQ-Q{row.id[-3:]}",
            "type": "faq_question",
            "level": "basic",
            "question": row.question,
            "gold_cards": [row.id],
            "gold_answers": [row.answer],
        }
        for row in df.itertuples(index=False)
    ]


def paraphrase_rows(evaluation: list[dict]) -> list[dict]:
    return [
        {
            "question_id": str(row["question_id"]),
            "type": "paraphrase",
            "level": "basic",
            "question": str(row["question"]),
            "gold_cards": [str(row["gold_faq_id"])],
            "gold_answers": [str(row["expected_answer"])],
        }
        for row in evaluation
        if row["answerable"]
    ]


def topic_groups(df: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    return list(df.groupby("topic", sort=True))


def topic_list_rows(df: pd.DataFrame) -> list[dict]:
    questions = []
    for topic, group in topic_groups(df):
        questions.append(
            {
                "question_id": f"TOPIC-{topic}",
                "type": "topic_list",
                "level": "basic",
                "question": f"Which FAQs cover the {topic} topic?",
                "gold_cards": group["id"].tolist(),
                "gold_answers": group["answer"].tolist(),
            }
        )
    return questions


def out_of_scope_rows(evaluation: list[dict]) -> list[dict]:
    rows = [
        {
            "question_id": str(row["question_id"]),
            "type": "out_of_scope",
            "level": "basic",
            "question": str(row["question"]),
            "gold_cards": [],
            "gold_answers": [],
        }
        for row in evaluation
        if not row["answerable"]
    ]
    rows.extend(
        [
            {
                "question_id": "OOS-003",
                "type": "out_of_scope",
                "level": "basic",
                "question": "Does DataPower support teleportation?",
                "gold_cards": [],
                "gold_answers": [],
            },
            {
                "question_id": "OOS-004",
                "type": "out_of_scope",
                "level": "basic",
                "question": "Which IBM product was announced in 2099?",
                "gold_cards": [],
                "gold_answers": [],
            },
        ]
    )
    return rows


def split_for(key: str) -> str:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return "heldout" if int(digest, 16) % 5 == 0 else "tuning"


def finish_rows(rows: list[dict]) -> list[dict]:
    finished = []
    for row in rows:
        key = row["gold_cards"][0] if row["gold_cards"] else row["question"]
        finished.append(
            {
                **row,
                "answerable": bool(row["gold_cards"]),
                "split": split_for(key),
            }
        )
    return finished


def build_basic_questions(records: list[dict[str, str]], evaluation: list[dict]) -> list[dict]:
    table = build_table(records)
    rows = faq_question_rows(table)
    rows.extend(paraphrase_rows(evaluation))
    rows.extend(topic_list_rows(table))
    rows.extend(out_of_scope_rows(evaluation))
    return finish_rows(rows)


def main() -> None:
    records = load_faqs(Path("data/faq.csv"))
    evaluation = load_evaluation(Path("data/evaluation.csv"))
    rows = build_basic_questions(records, evaluation)
    path = Path("data/eval/questions.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    table = pd.DataFrame(rows)
    print("rows:", len(rows))
    print("types:", table.groupby("type").size().to_dict())
    print("answerable:", table.groupby("answerable").size().to_dict())
    print("split:", table.groupby("split").size().to_dict())


if __name__ == "__main__":
    main()
