from pathlib import Path

from faq_agent.data import load_faqs
from faq_agent.embeddings import embed_texts, make_embedding_model
from faq_agent.index import faq_rows, save_rows

records = load_faqs(Path("data/faq.csv"))
rows = faq_rows(records)
vectors = embed_texts(make_embedding_model(), [row["text"] for row in rows])
for row, vector in zip(rows, vectors):
    row["vector"] = vector

path = Path("data/index/faq-vectors.jsonl")
save_rows(rows, path)
print("rows:", len(rows))
print("vector length:", len(rows[0]["vector"]))
print("file bytes:", path.stat().st_size)
