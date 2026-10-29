# faq_agent/metrics.py
from sklearn.metrics import f1_score, precision_score, recall_score


def retrieval_scores(
    gold: list[str], retrieved: list[str], universe: list[str]
) -> dict:
    actual = [int(code in gold) for code in universe]
    found = [int(code in retrieved) for code in universe]
    return {
        "precision": precision_score(actual, found, zero_division=0),
        "recall": recall_score(actual, found, zero_division=0),
        "f1": f1_score(actual, found, zero_division=0),
    }


def first_card_correct(gold: list[str], retrieved: list[str]) -> bool:
    return bool(retrieved and retrieved[0] in gold)
