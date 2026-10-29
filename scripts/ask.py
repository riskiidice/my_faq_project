# scripts/ask.py
import sys
from faq_agent.llm import call_model, make_client

question = " ".join(sys.argv[1:]) or "Does DataPower support SHA-2 certificates?"
result = call_model(make_client(), question, max_tokens=1024)

print("question:", question)
print("stop reason:", result["stop_reason"])
print(
    "tokens:", result["input_tokens"], result["cached_input_tokens"],
    result["output_tokens"],
)
print("seconds:", result["seconds"])
print("text:", result["text"])