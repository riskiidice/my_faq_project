import os
from pathlib import Path
from openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

client = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])


response = client.chat.send(
    model="deepseek/deepseek-v4.1-flash-1017",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Does DataPower support SHA-2 certificates?"}],
)

path = Path("data/responses/first-response.json")
path.write_text(response.model_dump_json(indent=2), encoding="utf-8")

print(response.choices[0].finish_reason)
print(not response.choices[0].message.content)