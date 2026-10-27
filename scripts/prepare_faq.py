import json
from pathlib import Path

all_source_rows = json.loads(
    Path("data/source/train.json").read_text(encoding="utf-8")
)

first_record = all_source_rows[0]

print("JSON type:", type(all_source_rows).__name__)
print("record count: ", len(all_source_rows))

first_answer = first_record["answer"]
print("first answer:", type(first_answer).__name__,
      len(first_answer), "characters")
print(
    "impossible records:",
    sum(row.get("is_impossible", False) for row in all_source_rows),
)
first_contexts = first_record["contexts"]
print(
    "first contexts:",
    str(first_contexts[0])[:60] + "...",
    type(first_contexts).__name__,
    len(first_contexts),
)

keep_fields = ["id", "question", "answer"]
impossible_source_ids = {
    row["id"] for row in all_source_rows if row.get("is_impossible", False)
}
source_rows = [
    {field: row.get(field) for field in keep_fields}
    for row in all_source_rows
    if not row.get("is_impossible", False)
]
print("Answerable records:", len(source_rows))
