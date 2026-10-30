# faq_agent/chunks.py
from faq_agent.data import faq_card


def topic_texts(records: list[dict[str, str]]) -> dict[str, str]:
    grouped = {}
    for record in records:
        topic = record["topic"]
        grouped.setdefault(topic, []).append(faq_card(record))
    return {topic: "\n\n".join(cards) for topic, cards in grouped.items()}

# faq_agent/chunks.py
def word_windows(text: str, size: int, overlap: int = 0) -> list[str]:
    if size < 1 or overlap < 0 or overlap >= size:
        raise ValueError("size must be positive and overlap must be smaller than size")
    words = text.split()
    step = size - overlap
    return [
        " ".join(words[start : start + size])
        for start in range(0, max(len(words) - overlap, 1), step)
    ]