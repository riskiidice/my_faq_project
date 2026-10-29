# scripts/measure_dense.py
from pathlib import Path
from time import perf_counter

import pandas as pd

from faq_agent import embeddings, index, metrics
from faq_agent.data import load_questions
from faq_agent.search import search_dense

QUESTIONS_PATH = Path("data/eval/questions.jsonl")
VECTOR_PATH = Path("data/index/faq-vectors.jsonl")


def basic_tuning_questions(questions: list[dict] | None = None) -> list[dict]:
    if questions is None:
        questions = load_questions(QUESTIONS_PATH)
    return [
        row for row in questions
        if row["level"] == "basic"
        and row["split"] == "tuning"
        and row["answerable"]
    ]


def score_question(
    question: dict,
    retrieved: list[str],
    retrieved5: list[str],
    universe: list[str],
) -> dict:
    scores = metrics.retrieval_scores(
        question["gold_cards"], retrieved, universe
    )
    recall5 = metrics.retrieval_scores(
        question["gold_cards"], retrieved5, universe
    )["recall"]
    return {
        "question_id": question["question_id"],
        "level": question["level"],
        "type": question["type"],
        **scores,
        "recall_at_5": recall5,
        "first_card_correct": metrics.first_card_correct(
            question["gold_cards"], retrieved
        ),
    }


def measure(
    questions: list[dict], rows: list[dict]
) -> tuple[pd.DataFrame, float]:
    model = embeddings.make_embedding_model()
    client = index.make_index(rows)
    universe = [row["id"] for row in rows]
    started = perf_counter()
    scores = []
    for question in questions:
        found = search_dense(
            model, client, question["question"], top_k=5
        )
        retrieved5 = [row["id"] for row in found]
        scores.append(
            score_question(question, retrieved5[:3], retrieved5, universe)
        )
    return pd.DataFrame(scores), perf_counter() - started


def report(scores: pd.DataFrame, seconds: float) -> None:
    print(
        f"overall n={len(scores)} precision={scores['precision'].mean():.3f} "
        f"recall={scores['recall'].mean():.3f} f1={scores['f1'].mean():.3f} "
        f"first_card_accuracy={scores['first_card_correct'].mean():.3f} "
        f"query_embedding_and_search_seconds={seconds:.1f}"
    )
    print("per-type first-card accuracy:")
    for name, group in scores.groupby("type", sort=True):
        print(f"{name}: {group['first_card_correct'].mean():.3f}")


def main() -> None:
    questions = basic_tuning_questions()
    rows = index.load_rows(VECTOR_PATH)
    scores, seconds = measure(questions, rows)
    report(scores, seconds)


if __name__ == "__main__":
    main()
