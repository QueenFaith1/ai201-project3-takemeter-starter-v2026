import csv

ai_labels = {
    82: "specific_question", 83: "general_question", 84: "general_question", 85: "general_question",
    86: "specific_question", 87: "specific_question", 88: "specific_question", 89: "general_question",
    90: "specific_question", 91: "specific_question", 92: "general_question", 93: "specific_question",
    94: "general_question", 95: "general_question", 96: "general_question", 97: "general_question",
    98: "general_question", 99: "general_question",
    102: "specific_question", 103: "specific_question", 104: "specific_question", 105: "specific_question",
    106: "general_question", 107: "general_question", 108: "specific_question", 109: "specific_question",
    110: "specific_question", 111: "specific_question", 112: "general_question", 113: "specific_question",
    114: "general_question", 115: "venting", 116: "venting", 117: "general_question",
    118: "specific_question", 119: "specific_question", 120: "specific_question", 121: "general_question",
    122: "specific_question", 123: "specific_question", 124: "specific_question", 125: "specific_question",
    126: "specific_question", 127: "general_question", 128: "specific_question", 129: "specific_question",
    130: "specific_question", 131: "general_question",
    132: "specific_question", 133: "general_question", 134: "venting", 135: "specific_question",
    136: "general_question", 137: "general_question", 138: "venting", 139: "specific_question",
    140: "specific_question", 141: "specific_question", 142: "general_question", 143: "general_question",
    144: "specific_question", 145: "general_question", 146: "venting", 147: "general_question",
    148: "specific_question", 149: "venting", 150: "venting", 151: "specific_question",
    152: "general_question", 153: "general_question", 154: "general_question", 155: "specific_question",
    156: "general_question", 157: "general_question", 158: "specific_question", 159: "general_question",
    160: "venting", 161: "specific_question", 162: "specific_question", 163: "general_question",
    164: "specific_question", 165: "general_question", 166: "specific_question", 167: "specific_question",
    168: "general_question", 169: "specific_question", 170: "general_question", 171: "general_question",
    172: "general_question", 173: "specific_question", 174: "venting", 175: "venting",
    176: "specific_question", 177: "specific_question", 178: "general_question", 179: "specific_question",
    180: "general_question", 181: "general_question", 182: "specific_question", 183: "general_question",
    184: "specific_question", 185: "specific_question", 186: "general_question", 187: "specific_question",
    188: "venting", 189: "venting", 190: "venting", 191: "general_question",
    192: "specific_question", 193: "venting", 194: "specific_question", 195: "specific_question",
    196: "general_question", 197: "general_question", 198: "specific_question", 199: "specific_question",
    200: "general_question", 201: "specific_question", 202: "general_question", 203: "general_question",
    204: "specific_question", 205: "general_question", 206: "specific_question", 207: "general_question",
    208: "general_question", 209: "specific_question", 210: "general_question", 211: "general_question",
    212: "specific_question", 213: "general_question",
}
# Rows 100 and 101 are the subreddit's sticky/mod posts, not real posts — left blank
# on purpose. We'll delete them from the file entirely once everything else is labeled.

with open("labels.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for i, label in ai_labels.items():
    rows[i]["label"] = label
    rows[i]["note"] = "ai-assisted"

with open("labels.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Filled in {len(ai_labels)} more rows. Total labeled so far: {sum(1 for r in rows if r['label'])}")