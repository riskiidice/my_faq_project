# faq_agent/prompts.py
ABSTAIN_TEXT = "I don't know"


def build_prompt(question: str, evidence: list[dict]) -> str:
    cards = "\n\n".join(row["text"] for row in evidence)
    return (
        "Use only the evidence below. If the evidence does not contain the answer, "
        f"reply exactly: {ABSTAIN_TEXT}.\n\n"
        f"Evidence:\n{cards}\n\nQuestion: {question}\nAnswer briefly:"
    )


def is_abstention(text: str) -> bool:
    return text.strip().lower().removesuffix(".") == ABSTAIN_TEXT.lower()
