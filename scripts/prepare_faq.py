# scripts/prepare_faq.py
import csv
import json
from pathlib import Path

all_source_rows = json.loads(
    Path("data/source/train.json").read_text(encoding="utf-8")
)

# EDA: look at the source before selecting
print("JSON type:", type(all_source_rows).__name__)
print("record count:", len(all_source_rows))
first_record = all_source_rows[0]
print("first record fields:", list(first_record))
print(
    "first ticket:",
    first_record["id"],
    first_record["question"].splitlines()[0],
)
first_answer = first_record["answer"]
print("first answer:", type(first_answer).__name__, len(first_answer), "characters")
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
faq_sources.extend([
    ("FAQ-009", "configuration", "TRAIN_Q000",
     "How can Streams use environment variables after an upgrade?"),
    ("FAQ-010", "configuration", "TRAIN_Q010",
     "Why does managesdk.sh report a file-lock error?"),
    ("FAQ-011", "configuration", "TRAIN_Q012",
     "What nproc value does WebSphere recommend on Linux?"),
    ("FAQ-012", "configuration", "TRAIN_Q016",
     "How can I display all hard or soft ulimit settings?"),
])
faq_sources.extend([
    ("FAQ-013", "troubleshooting", "TRAIN_Q014",
     "Why does the NMA agent fail to install on Linux?"),
    ("FAQ-014", "troubleshooting", "TRAIN_Q018",
     "Why does deleting a virtual portal time out?"),
    ("FAQ-015", "troubleshooting", "TRAIN_Q031",
     "How can DataPower handle a 302 redirect from a POST?"),
    ("FAQ-016", "troubleshooting", "TRAIN_Q053",
     "Why can't the Centera fixed content provider initialize?"),
])
print("Case file:", len(faq_sources), "of 16 found")
# EDA: count the case-file topics
topic_counts = {
    topic: sum(row[1] == topic for row in faq_sources)
    for topic in sorted({row[1] for row in faq_sources})
}
print("FAQs by topic:", topic_counts)

# EDA: inspect the selected answers
source_by_id = {row["id"]: row for row in source_rows}
for _, _, source_id, _ in faq_sources:
    if source_id in impossible_source_ids:
        raise ValueError(f"Source row {source_id} has no answer.")
    if source_id not in source_by_id:
        raise ValueError(f"Source row {source_id} is missing from train.json.")
    answer = source_by_id[source_id].get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError(f"Source row {source_id} has no answer.")

selected_answers = [
    source_by_id[source_id]["answer"] for _, _, source_id, _ in faq_sources
]
answer_lengths = [len(answer) for answer in selected_answers]
print(
    "selected answers with line breaks:",
    sum("\n" in answer for answer in selected_answers),
)
print("selected answer length range:", min(answer_lengths), max(answer_lengths))

prepared_rows = []
for faq_id, topic, source_id, question in faq_sources:
    source = source_by_id[source_id]
    answer = " ".join(source["answer"].split())
    if faq_id == "FAQ-012":
        answer = (
            "ulimit -Ha displays all hard limits, and ulimit -Sa displays all "
            "soft limits for the current login session. In the source TechQA "
            "answer, X is a placeholder for H (hard) or S (soft); do not type "
            "X literally."
        )
    prepared_rows.append((faq_id, topic, question, answer))

print("Prepared FAQs:", len(prepared_rows))
output_path = Path("data/faq.csv")

with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(("id", "topic", "question", "answer"))
    writer.writerows(prepared_rows)

print("Output:", output_path)
