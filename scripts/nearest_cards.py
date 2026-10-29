import sys
from pathlib import Path

from faq_agent.data import faq_card, load_faqs
from faq_agent.embeddings import cosine_similarity, embed_texts, make_embedding_model


def main():
    records = load_faqs(Path("data/faq.csv"))
    cards = [faq_card(record) for record in records]
    model = make_embedding_model()
    vectors = embed_texts(model, cards)
    question = " ".join(sys.argv[1:]) or "Does DataPower support SHA-2 certificates?"
    question_vector = embed_texts(model, [question])[0]
    scores = [
        (cosine_similarity(question_vector, vector), record["id"])
        for record, vector in zip(records, vectors)
    ]
    for score, name in sorted(scores, reverse=True)[:3]:
        print(f"{name} {score:.3f}")


if __name__ == "__main__":
    main()