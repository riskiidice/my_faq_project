# scripts/compare_chunks.py
from pathlib import Path

from faq_agent.chunks import cards_kept_whole, topic_texts, word_windows
from faq_agent.data import faq_card, load_faqs

# scripts/compare_chunks.py
STRATEGIES = [
    ("30-word windows", 30, 0),
    ("60-word windows", 60, 0),
    ("60 words, overlap 10", 60, 10),
    ("120-word windows", 120, 0),
    ("120 words, overlap 20", 120, 20),
]


def format_row(label: str, chunks: int, kept: int, total: int) -> str:
    return f"{label:<24} {chunks:>6} {kept}/{total} ({kept / total:.1%})"


def main():
    records = load_faqs(Path("data/faq.csv"))
    cards = [faq_card(record) for record in records]
    documents = topic_texts(records)
    print(f"{'Strategy':<24} {'Chunks':>6} Cards kept whole")
    for label, size, overlap in STRATEGIES:
        chunks = [chunk for text in documents.values()
                  for chunk in word_windows(text, size, overlap)]
        kept = cards_kept_whole(cards, chunks)
        print(format_row(label, len(chunks), kept, len(cards)))
    print(format_row("one chunk per FAQ", len(cards),
                     cards_kept_whole(cards, cards), len(cards)))


if __name__ == "__main__":
    main()
