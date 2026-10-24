import csv

# Matches on each post's distinctive opening line — safer than retyping full text.
FLIPS = {
    "Should I dip into trust to pay off debt?": "specific_question",
    "I\u2019m feeling pretty lost about my finances and worried about my future.": "specific_question",
    "22 y/o looking for Guidance + Next Steps": "specific_question",
    "Retirement and inflation question": "specific_question",
    "I am 26 and have 1k to my name": "specific_question",
}

with open("labels.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

changed = 0
for row in rows:
    for opener, new_label in FLIPS.items():
        if row["text"].startswith(opener):
            old = row["label"]
            row["label"] = new_label
            row["note"] = (row["note"] + "; " if row["note"] else "") + "relabeled: venting->specific_question (M5 boundary fix)"
            print(f"Changed: '{opener[:50]}...'  {old} -> {new_label}")
            changed += 1

with open("labels.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    writer.writeheader()
    writer.writerows(rows)

print(f"\nTotal changed: {changed} (expected 5)")