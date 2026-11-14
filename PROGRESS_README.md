# Break the Model — Progress Tracker

Live board of our entry for the **Entropy Alignment Security** hackathon: a sanctioned red-team of
**Riley**, the AI front-desk assistant of the fictional *Scioto Ridge* hospital (fake synthetic
data, chat-only attacks).

- **Live board:** `index.html` (served via GitHub Pages — link in the repo's About/Settings).
- **Source of truth:** `status.json`. The page renders from it.

## How to update the board

Everything on the dashboard comes from **`status.json`**. To record progress:

1. Edit `status.json` (models, attacks, levels, defense, SSN, `next`).
2. Bump `meta.updated` to the current UTC timestamp.
3. Re-embed the JSON into the page so it also works offline (optional on Pages — the page fetches
   `status.json` live — but keeps the single-file/Artifact view correct):
   ```bash
   python embed.py
   ```
4. Commit `status.json` (and `index.html` if you re-embedded) and push.

> The page loads the embedded copy first, then overrides it with a live `fetch("status.json")` when
> served over HTTP (GitHub Pages). So on Pages, editing `status.json` alone is enough.

## Field reference (`status.json`)

| Key | What it drives |
|---|---|
| `meta` | Title, subtitle, target, `updated` timestamp |
| `headline` | The amber summary banner |
| `levels[]` | `{id,name,status}` — status one of `cleared` / `holds` / `disputed` / `open` |
| `models[]` | `{name,tag?,a1,a2,a3,verdict}` — rate strings colour themselves (100 → green, 40–89 → amber, else red, `resist` → grey) |
| `attacks[]` | `{id,name,idea,result}` — a `result` containing "retract" is styled as retracted |
| `leaks` | `{obtained,not_obtained}` |
| `ssn` | `{status,detail}` |
| `defense` | `{file,status,layers[],gap}` |
| `next[]` | Open tasks |

## Full writeups (not on the board)

- `FINDINGS.md` — complete results, turn_ids, Level 3 analysis, defense measurements.
- `HANDOFF.md` — take-over guide (setup, what works per model).
- `DEEPSEEK_PROGRESS_participant-claude.md` — DeepSeek methods, rates, SSN ledger.
- `SLIDES.md` — 3-minute pitch outline.
- `break-the-model-capsule.md` — merged master context capsule.

All attack evidence is in `logs/my_attempts.jsonl` (turn_id per call).
