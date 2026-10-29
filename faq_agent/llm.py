import os
import time
from dotenv import load_dotenv
from openrouter import OpenRouter
from openrouter.utils import BackoffStrategy, RetryConfig

MODEL = "deepseek/deepseek-v4.1-flash-1017"
NO_RETRY = RetryConfig("none", BackoffStrategy(1, 1, 1.0, 1), False)

load_dotenv()

def make_client() -> OpenRouter:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENROUTER_API_KEY in your terminal.")
    return OpenRouter(api_key=api_key, retry_config=NO_RETRY)

def call_model(
    client, user_text: str, max_tokens: int, *, model: str = MODEL
) -> dict:
    started = time.perf_counter()
    response = client.chat.send(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": user_text}],
    )
    details = getattr(response.usage, "prompt_tokens_details", None)
    return {
        "text": response.choices[0].message.content or "",
        "seconds": round(time.perf_counter() - started, 2),
        "input_tokens": response.usage.prompt_tokens,
        "cached_input_tokens": getattr(details, "cached_tokens", 0) or 0,
        "output_tokens": response.usage.completion_tokens,
        "stop_reason": response.choices[0].finish_reason,
        "response_model": response.model,
    }