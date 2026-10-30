from faq_agent.metrics import first_card_correct
from faq_agent.metrics import retrieval_scores

scores = retrieval_scores(["A", "B"], ["A", "C", "D"], list("ABCDEF"))
for name, value in scores.items():
    print(f"{name}: {value:.3f}")


print("first card:", first_card_correct(["A", "B"], ["C", "A"]))
print("first card:", first_card_correct(["A", "B"], ["B", "C"]))
