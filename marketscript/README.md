# MarketScript

**A Claude Code skill that turns plain-English marketing data tasks into annotated, explainable Python scripts.**

---

## What It Is

MarketScript is a structured prompt skill for Claude Code. You describe a marketing data task in plain English — grouping sales data, filtering survey responses, ranking store revenue — and Claude returns a complete Python script alongside a plain-English explanation of every step, a list of data assumptions to verify, and a short paragraph you could use to explain the script in a job interview.

The output is split into four labeled sections every time:

1. **Python Code** — a complete, runnable script in a fenced code block, with short step labels
2. **Section-by-Section Explanation** — plain English walkthrough of each step, written for someone with no coding background
3. **Assumption Warnings** — every column name, file path, data type, and format the code assumes about your data
4. **Interview Summary** — a 3–5 sentence first-person paragraph you can read aloud to explain the script confidently, with no mention of AI

---

## The Problem It Solves

Code generation tools already exist. ChatGPT, Copilot, and others can produce working Python scripts on demand. The problem is not writing the code — it is that the output is a black box. If you did not write it, you cannot read it, cannot verify it, cannot catch errors before running it on real data, and cannot explain it to an interviewer or a manager.

MarketScript is built for the opposite user: someone who knows what they want to accomplish but has no way to evaluate whether the generated code actually does it. The explanation layer is the core feature, not a bonus. It closes the gap between generating code and understanding it.

### Two separate loops

MarketScript treats understanding and changing as two distinct workflows:

| Loop | Trigger | What changes |
|---|---|---|
| **Explanation loop** | "I don't understand this step" | Only the plain-English explanation for that step — the code stays the same |
| **Code refinement loop** | "Group by region instead of category" | The code updates, and the explanations refresh to match |

This order is intentional. Understand the script first. Then decide what to change.

---

## How to Invoke It in Claude Code

### Option 1 — Reference the skill file directly

Open Claude Code in the `marketscript` project directory and paste or attach the contents of `SKILL.md` at the start of your session. Then describe your task:

```
[paste SKILL.md contents]

My task: I have a CSV with customer IDs, purchase amounts, and store locations.
Calculate total revenue by store and rank them highest to lowest.
```

### Option 2 — Use as a slash command

If you have set up Claude Code custom commands, save `SKILL.md` as a command file (e.g., `.claude/commands/marketscript.md`) so you can invoke it with:

```
/marketscript I have a CSV with customer IDs, purchase amounts, and store locations. Calculate total revenue by store and rank them highest to lowest.
```

### Option 3 — Inline invocation

At the start of any Claude Code session, tell Claude to follow the MarketScript skill:

```
Follow the MarketScript skill in marketscript/SKILL.md and respond to this task:
"I have a CSV with purchase amounts and store locations. Rank stores by total revenue."
```

---

## Example Session

**User:**
> I have a CSV with customer IDs, purchase amounts, and store locations. Calculate total revenue by store and rank them highest to lowest.

**Claude returns:**
- Complete Python script using pandas, labeled by step
- Plain-English explanation of each step (imports, load data, group, rank, export)
- Assumption Warnings listing exact column names the code expects
- Interview Summary paragraph

**User asks a follow-up on the explanation:**
> I don't understand what groupby is doing in step 3.

**Claude rewrites only that explanation.** The code does not change.

**User then refines the code:**
> Now also show the average purchase amount per store.

**Claude updates the code and refreshes all explanations to match.**

---

## Files in This Folder

| File | Purpose |
|---|---|
| `SKILL.md` | The full skill instructions Claude follows when generating MarketScript output |
| `README.md` | This file — overview, problem statement, and invocation guide |

---

## Project Context

MarketScript was built as a final project for MKTG 490 (Spring 2026). The live browser-based prototype lives in `index.html` in the project root — a single self-contained HTML file that calls the OpenAI API directly from the browser with no backend required. This skill file brings the same structured output format into Claude Code as a reusable, invokable skill.
