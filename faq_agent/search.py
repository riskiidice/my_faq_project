from faq_agent.embeddings import embed_texts
from faq_agent.index import search_vectors


def search_dense(model, client, question: str, top_k: int = 3) -> list[dict]:
    vector = embed_texts(model, [question])[0]
    return search_vectors(client, vector, top_k)
