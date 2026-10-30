# scripts/answer_examples.py
from pathlib import Path

from faq_agent import embeddings, index, llm, prompts, search

QUESTIONS = (
    "Does DataPower support SHA-2 certificates?",
    "Can DataPower handle a 302 redirect from a POST request?",
    "Does DataPower support teleportation?",
)


def show_answer(question, model, client, vector_index):
    evidence = search.search_dense(model, vector_index, question)
    result = llm.call_model(
        client, prompts.build_prompt(question, evidence), max_tokens=1024
    )
    print("question:", question)
    print("retrieved:", ", ".join(row["id"] for row in evidence))
    print("answer:", result["text"])
    print("abstained:", prompts.is_abstention(result["text"]))
    return result["seconds"]


def main():
    rows = index.load_rows(Path("data/index/faq-vectors.jsonl"))
    vector_index = index.make_index(rows)
    model, client = embeddings.make_embedding_model(), llm.make_client()
    seconds = sum(show_answer(q, model, client, vector_index)
                  for q in QUESTIONS)
    result = llm.call_model(client, QUESTIONS[-1], max_tokens=1024)
    print("without evidence:", QUESTIONS[-1], "->", result["text"])
    print("total model seconds (4 calls):",
          round(seconds + result["seconds"], 1))


if __name__ == "__main__":
    main()
