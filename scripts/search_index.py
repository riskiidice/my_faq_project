# scripts/search_index.py
import sys
from pathlib import Path

from faq_agent.embeddings import embed_texts, make_embedding_model
from faq_agent.index import load_rows, make_index, search_vectors

rows = load_rows(Path("data/index/faq-vectors.jsonl"))
client = make_index(rows)
question = " ".join(
    sys.argv[1:]) or "Does DataPower support SHA-2 certificates?"
vector = embed_texts(make_embedding_model(), [question])[0]
results = search_vectors(client, vector, 3)
for row in results:
    print(f"{row['id']} {row['topic']} {row['score']:.3f}")
