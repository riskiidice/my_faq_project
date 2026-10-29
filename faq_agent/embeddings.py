import math

from fastembed import TextEmbedding

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(left * right for left, right in zip(a, b))
    length_a = math.sqrt(sum(value * value for value in a))
    length_b = math.sqrt(sum(value * value for value in b))
    if not length_a or not length_b:
        return 0.0
    return dot / (length_a * length_b)

def make_embedding_model() -> TextEmbedding:
    return TextEmbedding(EMBEDDING_MODEL, cache_dir="data/models")


def embed_texts(model: TextEmbedding, texts: list[str]) -> list[list[float]]:
    return [vector.tolist() for vector in model.embed(texts)]