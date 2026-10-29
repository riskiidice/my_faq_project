import json
from faq_agent.data import faq_card
from pathlib import Path

from qdrant_client import QdrantClient, models


def faq_rows(records: list[dict]) -> list[dict]:
    return [
        {
            "id": record["id"],
            "topic": record["topic"],
            "question": record["question"],
            "answer": record["answer"],
            "text": faq_card(record),
        }
        for record in records
    ]


def save_rows(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

def make_index(rows: list[dict]) -> QdrantClient:
    client = QdrantClient(":memory:")
    client.create_collection("faqs", vectors_config=models.VectorParams(
        size=len(rows[0]["vector"]), distance=models.Distance.COSINE))
    client.upsert("faqs", points=[
        models.PointStruct(id=i, vector=row["vector"],
            payload={key: row[key] for key in ("id", "topic", "question", "answer", "text")})
        for i, row in enumerate(rows)
    ])
    return client

def search_vectors(client, vector: list[float], top_k: int) -> list[dict]:
    points = client.query_points(
        "faqs", query=vector, limit=top_k, with_payload=True
    ).points
    return [
        {**p.payload, "score": p.score}
        for p in points
    ]
