import json
from pathlib import Path

response = json.loads(
    Path("data/responses/first-response.json").read_text(encoding='utf-8')
)
choice = response["choices"][0]
print("id:", response["id"])
print("model:", response["model"])
print(choice["message"]["content"] or "(no text)")
print("finish reason:", choice["finish_reason"])
usage = response["usage"]
names = sorted(usage)
print(names)
print("usage keys:", len(names))
print(usage["prompt_tokens"], usage["completion_tokens"])
