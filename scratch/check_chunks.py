# scratch: check_chunks.py
from faq_agent.chunks import topic_texts, word_windows
from pathlib import Path

from faq_agent.data import load_faqs

records = load_faqs(Path("data/faq.csv"))
texts = topic_texts(records)
words = [len(text.split()) for text in texts.values()]
sizes = {name: text.count("\n\n") + 1 for name, text in texts.items()}
print("topic texts:", len(texts))
print(f"words: min={min(words)} max={max(words)} mean={round(sum(words) / len(words), 1)}")
largest = max(texts, key=lambda name: len(texts[name].split()))
smallest = min(texts, key=lambda name: len(texts[name].split()))
print("largest:", largest, max(sizes.values()), "FAQs")
print("smallest:", smallest, min(sizes.values()), "FAQs")


print(word_windows("a b c d e", 2))
print(word_windows("a b c d e", 2, 1))
try:
    word_windows("a b c", 2, 2)
except ValueError as error:
    print(type(error).__name__, error)