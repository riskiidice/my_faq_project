# faq_agent/rag.py
from faq_agent.llm import call_model
from faq_agent.prompts import build_prompt, is_abstention
from faq_agent.search import search_dense

def answer(question: str, model, index, llm_client, top_k: int = 3) -> dict:
    evidence = search_dense(model, index, question, top_k)
    result = call_model(llm_client, build_prompt(question, evidence), max_tokens=1024)
    return {
        "question": question, "answer": result["text"],
        "abstained": is_abstention(result["text"]), "evidence": evidence,
        **{key: result[key] for key in (
            "seconds", "input_tokens", "cached_input_tokens",
            "output_tokens", "stop_reason",
        )},
    }