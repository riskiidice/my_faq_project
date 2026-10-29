import pandas as pd


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
