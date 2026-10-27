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


keyword = "candledata"
for row in source_rows:
    if keyword in row["question"].lower():
        print(row["id"], row["question"].splitlines()[0])


faq_sources = [
    ("FAQ-001", "product_info", "TRAIN_Q030",
     "Does DataPower support SHA-2 certificates?"),
    ("FAQ-002", "product_info", "TRAIN_Q046",
     "Does the Linux KVM monitoring agent support CANDLEDATA?"),
    ("FAQ-003", "product_info", "TRAIN_Q056",
     "What does wpcollector do in WebSphere Portal?"),
    ("FAQ-004", "product_info", "TRAIN_Q066",
     "Is a 64-bit Log File Agent available for Windows?"),
]
faq_sources.extend([
    ("FAQ-005", "compatibility", "TRAIN_Q008",
     "Is RequisitePro supported by 64-bit RAD or RSA?"),
    ("FAQ-006", "compatibility", "TRAIN_Q013",
     "Can a TIP 2.2 fix pack be installed directly on TIP 2.1?"),
    ("FAQ-007", "compatibility", "TRAIN_Q017",
     "Which Oracle version is listed for Portal 6.1.0.6?"),
    ("FAQ-008", "compatibility", "TRAIN_Q050",
     "Does JazzSM 1.1.2.1 support HTTP access?"),
])
print("Case file:", len(faq_sources), "of 16 found")
print("Product info tickets:", sum(
    row[1] == "product_info" for row in faq_sources))
