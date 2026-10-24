# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This project sorts posts from r/personalfinance into three categories: `specific_question` (the poster needs a tailored answer based on their own numbers or accounts), `general_question` (a real question that doesn't depend on the poster's specific figures, process, legality, or "is this normal" questions), and `venting` (no real question, just a personal story, PSA, or emotional post). A classifier like this could help a subreddit's moderators or a bot route posts appropriately,  flagging specific_question posts for financially literate volunteers who can do the math, routing general_question posts toward existing wiki resources, and leaving venting posts alone rather than flooding them with unsolicited advice.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `general_question`

**Definition:** Asks a question whose answer doesn't depend on the poster's numbers.


**Example 1:**https://www.reddit.com/r/personalfinance/
>My question is what now?

**Example 2:** https://www.reddit.com/r/personalfinance/comments/1wbkqbi/received_an_inheritance_and_husband_is_getting/
>is there anything else we need to talk about or plan?

### `specific_question`

**Definition:** Asks a question and includes the posters own numbers or named accounts. 

**Example 1:** https://www.reddit.com/r/personalfinance/comments/1x516fj/how_much_to_save_in_hysa_vs_invest/
> I have about 46k in investments and 14k in HYSA.

**Example 2:**https://www.reddit.com/r/personalfinance/comments/1mduljg/needing_general_money_advice/
>I'm 2000$ (one card) in credit card debt, totally maxed out.

### `Venting`

**Definition:** Describes feelings about money and doesn't ask a question.


**Example 1:** https://www.reddit.com/r/personalfinance/comments/1286ao5/age_32_57k_in_student_loan_debt_should_i_pay_it/
> This is causing me tons of anxiety and I'm not even the borrower.

**Example 2:**https://www.reddit.com/r/personalfinance/comments/1t17vz4/i_cant_stop_thinking_about_things_per_hour/
>I guess I'm just venting.
    

### The hardest boundary

**Which two labels:** `specific_question` and `general_question`, when a post asks a question that has an underlying general topic but includes the poster's own numbers.


**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If the post asks a question, check for the poster's own numbers. With numbers, it's `specific_question`. Without, it's `general_question`. No question at all means `venting`.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

I collected posts from r/personalfinance (Reddit), pulling the text of the post titles and bodies into `labels.csv`.

**Labels:**
`specific_question`   needs a tailored answer based on the poster's own numbers/situation (e.g. "given these balances, should I pay off X or invest in Y")
 `general_question` a real question, but answerable without the poster's specific figures (process, legality, "is this normal" questions)
-`venting` — no real question being asked, just a personal story, PSA, or emotional post


**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

 I hand labeled the first 20 posts cold, with no AI assistance, as a baseline check on my own judgment before defining any process. For the remaining  192 posts, I gave Claude my label definitions (specific_question: needs a tailored answer based on the poster’s own numbers/situation; general_question: a real question, but answerable without the poster’s specific figures, process, legality, or “is this normal” questions; venting: no real question being asked, just a personal story, PSA, or emotional post) and had it produce a first pass. I then read every single AI-labeled row myself and corrected any I disagreed with before committing. Rows labeled this way are marked ai assisted in the note column. Two posts (the subreddit’s sticky “welcome” and weekly “help and victory” threads) were excluded entirely as non-posts, leaving 212 labeled rows: 102 general_question (48%), 89 specific_question (42%), 21 venting (10%), no label above 70%.


*Counts (212 labeled rows):**
| Label | Count | % |
|---|---|---|
| general_question | 102 | 48% |
| specific_question | 89 | 42% |
| venting | 21 | 10% |

No label exceeds 70%.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->
**Three hard cases:**

1. **"I feel so behind financially"** (31F, $12/hr, no debt) — has real numbers and asks for advice, but ends *"I suppose I am just venting."* I labeled it `venting` on the strength of that line, over `general_question`.

2. **"Watched my company stock sink 50%"** — asks a real financial question (sell/hold/diversify) but spends more of the post on emotional distress ("how did you pull yourself out of that dark headspace?"). I went with `general_question` since the financial ask doesn't need the poster's specific numbers to answer, but `venting` was a close second.

3. **"I'm an heir to a broke aunt"** — a long, detailed personal story (dying aunt, ~$500/month mortgage, unknown credit card debt) that lands on a general legal question: *"do heirs inherit credit card debt?"* I labeled it `general_question` since the answer doesn't depend on her specific numbers, though her numbers are clearly what's driving the question.


<!-- Your starting model, your settings, and anything you changed and why. -->

## The Training Run

**Base model:** distilbert-base-uncased

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max_length 128, seed 42

**Anything I changed from the defaults, and why:** Nothing — used the defaults as given.

**Split sizes:** train 148 / val 32 / test 32. `venting` has only 3 examples in the test split (vs. 14-15 for the other two labels), well under the ~8 needed for a stable metric — its F1 is expected to be noisy across seeds.

**Device:** CPU, torch 2.14.1+cpu. Recorded in `results.json`.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*Pre-labeling for the remaining ~192 posts in `to_label.txt`, using my label definitions (specific_question / general_question / venting) and decision rule (own numbers + question → specific; question with no own numbers → general; no question → venting).
- *What came back:*  A Python dict mapping row index → label, formatted to drop directly into my `parse_posts.py`. 

- *What I changed:* I read every AI-labeled row against the original post text myself and corrected any I disagreed with before merging it into `labels.csv`. Those rows are marked `ai-assisted` in the note column.
vice: CPU, torch 2.14.1+cpu

**Moment 2**

- *What I asked for:* Help debugging `parse_posts.py`, which kept failing with `SyntaxError: '{' was never closed` after I pasted the label dict into VS Code.
- *What came back:*  Confirmation the dict's syntax was valid on Claude's end (ruling out a bad dict), then a PowerShell one-liner that decoded a base64-encoded copy of the script straight to disk.
- *What I changed:* Used that approach instead of re-pasting into the editor, which is what actually fixed it — the editor's auto-bracket-matching had been corrupting the paste.

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->


| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.469 | 0.562 | +0.094 |
| Macro F1 | 0.276 | 0.345 | +0.069 |
| F1 — `general_question` | 0.222 | 0.682 | +0.460 |
| F1 — `specific_question` | 0.605 | 0.353 | -0.252 |
| F1 — `venting` | 0.000 | 0.000 | +0.000 |


**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
I expected the trained model to beat the baseline
most on `venting` (baseline F1 = 0.000) and `general_question` (baseline F1 =
0.222), since both show the general model struggling without task-specific
training.
**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

Fine-tuning added real value, but unevenly. Overall accuracy and macro F1 moved
only modestly (+0.094, +0.069) because the gains on `general_question` were
offset by a loss on `specific_question` — the one label the untrained model
already handled well. That's not "fine-tuning added nothing," but it's also not
a clean win across the board: training on my data taught the model
`general_question` at the cost of some of what the baseline already knew
about `specific_question`. `venting` is inconclusive either way — n=3 in the
test split is too small to credit the model with learning it or blame it for
failing to.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

     ## Run Log — Before

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.562 | 0.500 | 0.469 | MISSED |
| 2. Every label F1 | ≥ 0.50 | general_question 0.682, specific_question 0.353, venting 0.000 | macro F1 only: 0.262 | macro F1 only: 0.213 | MISSED |
| 3. Largest label share | ≤ 70% of labels.csv | 48% (dataset-level, same all seeds) | — | — | MET |
| 4. Cold-relabel agreement | ≥ 80% | 30% (6/20) | — | — | MISSED |
| 5. Each label ≥ 6 in test split | ≥ 6 | general_question 15, specific_question 14, venting 3 | not broken out per seed | not broken out per seed | MISSED |

### Confusion matrix

| true \ predicted | specific_question | general_question | venting |
|---|---|---|---|
| **specific_question** | 3 | 11 | 0 |
| **general_question** | 0 | 15 | 0 |
| **venting** | 0 | 3 | 0 |

**My biggest off-diagonal number, and what it means:**

The model misclassified 11 of 14 real `specific_question` posts as `general_question`,
while making zero errors in the opposite direction — it's defaulting to
`general_question` whenever a post is ambiguous, rather than confusing the
two labels symmetrically.

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 | MISSED | All three seeds (0.562, 0.500, 0.469) fell short; target must hold across all three. |
| 2 | Every label F1 | ≥ 0.50 | MISSED | On seed 42, `specific_question` (0.353) and `venting` (0.000) both fall well short. |
| 3 | Largest label ≤ 70% | ≤ 70% | MET | `general_question` is 48% of labels.csv. |
| 4 | Cold-relabel agreement | ≥ 80% | MISSED | Relabeled my 20 cold posts blind; agreed with myself on only 6/20 (30%). |
| 5 | Each label ≥ 6 in test split | ≥ 6 | MISSED | `venting` has only 3 in the one split I measured (10% of 212 rows total). |

**Diagnoses**

My own agreement report is the clearest evidence here, and it points at a labeling problem, not just a model limitation. When I relabeled my original 20 cold posts blind, I agreed with myself on only 30% — and every post I originally called `venting` (5 of 5), I relabeled as `general_question` or `specific_question` the second time. That's the same direction the model's confusion matrix shows: it also collapses toward `general_question`, especially away from `specific_question`.

So criteria 1 and 2 (accuracy and per-label F1) are diagnosed as a **boundary applied inconsistently**: the model can't learn a clean `venting` vs. `general_question` line from training data where I wasn't drawing that line the same way twice myself. Criterion 5 (venting's test coverage) is a separate, compounding cause — **too few examples for a label** (only 21 of 212 rows), which makes the already-inconsistent boundary even harder for the model to learn reliably.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
