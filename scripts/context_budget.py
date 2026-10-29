# scripts/context_budget.py
from pathlib import Path
from faq_agent.context import evidence_budget, fits_context
from faq_agent.data import faq_card, load_faqs
from faq_agent.llm import call_model, make_client

CONTEXT_LIMIT_TOKENS = 4096
ANSWER_RESERVE = 1024

record = load_faqs(Path("data/faq.csv"))[0]
card = faq_card(record)
prompt = f"Use this FAQ card to answer: {record['question']}\n\n{card}"
result = call_model(make_client(), prompt, max_tokens=1024)
counts = result["input_tokens"], result["cached_input_tokens"]
print("prompt chars/input/cache/total:", len(prompt), *counts, sum(counts))
print("answer:", result["text"])

ratio = len(prompt) / sum(counts)
card_tokens = round(len(card) * sum(counts) / len(prompt))
room = evidence_budget(CONTEXT_LIMIT_TOKENS, sum(counts), ANSWER_RESERVE)
fits = fits_context(
    CONTEXT_LIMIT_TOKENS, sum(counts), ANSWER_RESERVE, card_tokens
)
print("characters/token, estimated tokens/card:", round(ratio, 2), card_tokens)
print("room/fits/total cards:", room, fits, 1 + room // card_tokens)