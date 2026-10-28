# scripts/prepare_faq.py
import argparse
import csv
import json
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Prepare the local TechQA FAQ CSV.")
parser.add_argument(
    "--full",
    action="store_true",
    help="write every complete, answerable source row to data/faq-full.csv",
)

parser.add_argument(
    "--report", action="store_true", help="show a report about the FAQ tables"
)

args = parser.parse_args()

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
print("selected answer length range:", min(
    answer_lengths), max(answer_lengths))

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

if args.full:
    impossible_count = len(impossible_source_ids)
    blank_question_count = sum(
        not isinstance(row.get("question"), str)
        or not row["question"].strip()
        for row in all_source_rows
    )
    blank_answer_count = sum(
        not isinstance(row.get("answer"), str) or not row["answer"].strip()
        for row in all_source_rows
    )
    full_rows = []
    for source in source_rows:
        raw_question = source.get("question")
        raw_answer = source.get("answer")
        if (
            not isinstance(raw_question, str)
            or not isinstance(raw_answer, str)
            or not raw_question.strip()
            or not raw_answer.strip()
        ):
            continue
        full_rows.append(source)
    print("impossible source rows:", impossible_count)
    print("blank source questions:", blank_question_count)
    print("blank source answers:", blank_answer_count)
    print("complete answerable source rows:", len(full_rows))

    selected_source_ids = {source_id for _, _, source_id, _ in faq_sources}
    for source in full_rows:
        source_id = source["id"]
        if source_id in selected_source_ids:
            continue
        question = " ".join(source["question"].split())
        answer = " ".join(source["answer"].split())
        prepared_rows.append(
            (f"TECHQA-{source_id}", "unclassified", question, answer)
        )


print("Prepared FAQs:", len(prepared_rows))
output_path = Path("data/faq-full.csv" if args.full else "data/faq.csv")

with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(("id", "topic", "question", "answer"))
    writer.writerows(prepared_rows)

print("Output:", output_path)
if args.full:
    guided_count = sum(row[0].startswith("FAQ-") for row in prepared_rows)
    print("Guided FAQs:", guided_count)


if args.report:
    df = pd.read_csv("data/faq.csv")
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    df['answer_chars'] = df['answer'].str.len()
    print(df[["id", "topic", "answer_chars"]].head(3).to_string(index=False))
    missing = df.isna().sum()
    print("missing value by columns:")
    print(missing[missing > 0].to_string())
    blank_answers = df["answer"].fillna("").str.strip().eq("").sum()
    print("blank answers:", blank_answers)
    print("FAQs by topic:")
    print(df["topic"].value_counts().sort_index().to_string())
    print("average answer characters by topic:")
    print(df.groupby("topic")['answer_chars'].mean().round(1))
    full_df = pd.read_csv("data/faq-full.csv")
    print("guided sample rows:", len(df))
    print("full answerable rows:", len(full_df))
    print("additional real source rows:", len(full_df) - len(df))
    print(
        "unclassified full-corpus rows:",
        int(full_df["topic"].eq("unclassified").sum()),
    )
    guided_ids = set(df["id"])
    print("guided IDs present in full:", int(
        full_df["id"].isin(guided_ids).sum()))
    longest = df.loc[df["answer_chars"].idxmax()]
    shortest = df.loc[df["answer_chars"].idxmin()]
    print("longest answer:", longest["id"], int(longest["answer_chars"]))
    print("shortest answer:", shortest["id"], int(shortest["answer_chars"]))

    raise SystemExit(0)
