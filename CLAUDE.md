# CLAUDE.md

Guidance for Claude when working in this repo. For the "why" (mission, scope, non-goals), read [CHARTER.md](CHARTER.md). For user-facing intro and dataset documentation, see [README.md](README.md).

## What this is

A static single-page web app that filters Japanese vocabulary by the user's *Remembering the Kanji* chapter progress. Three CSV datasets, one HTML file with embedded CSS/JS, no build step, deployed to GitHub Pages.

## Files

- [index.html](index.html) — the entire web app (HTML + CSS + JS in one file)
- [jp_freq_translation_reading.csv](jp_freq_translation_reading.csv) — vocabulary used by the website (Leeds Corpus + Heisig mapping, with `kana_tier` and `kind` columns added by the migration)
- [heisig_kanjis.csv](heisig_kanjis.csv) — kanji → Heisig number/chapter reference
- [jokugos_freq_db_heisig_hiragana.csv](jokugos_freq_db_heisig_hiragana.csv) — 2-kanji compound words (not currently consumed by the site; see FUTURE_PLANS.md "Considered, declined")
- [tools/](tools/) — one-shot scripts for dataset migrations (e.g. `migrate_kana_tiers.py`). Idempotent where possible. Not consumed by the website at runtime.
- [README.md](README.md) — user-facing intro and dataset documentation
- [CHARTER.md](CHARTER.md) — project mission, scope, non-goals, pedagogical foundation
- [FUTURE_PLANS.md](FUTURE_PLANS.md) — working roadmap and decision log
- [LICENSE](LICENSE) — MIT, covers source code only.
- [LICENSE-DATA](LICENSE-DATA) — CC BY 4.0, covers the CSV datasets (with full attribution chain to the Leeds upstream).

## How to work here

- **No build system, no package manager, no tests.** The site is plain HTML/CSS/JS plus PapaParse loaded from CDN. Don't introduce a build step, framework, or dependency casually — if a feature genuinely needs one, raise it explicitly and check it against [CHARTER.md](CHARTER.md).
- **Datasets are load-bearing artifacts.** They were hand-curated, and the website depends on their schema. Do not regenerate, reorder, or modify them as a side effect of feature work. Schema changes (new columns, new rows, retagging) happen via **deliberate, one-shot migrations** with their own scripts in [tools/](tools/), recorded in [FUTURE_PLANS.md](FUTURE_PLANS.md). The kana tier migration is the canonical example.
- **CSV delimiter is `;`** (not `,`). PapaParse calls and any new tooling must respect this.
- **State lives in the browser.** No accounts, no server-side persistence today. If a feature seems to need either, see [CHARTER.md](CHARTER.md) — it's a current stance, not a closed door, but changing it is a deliberate decision.
- **Run locally** by serving the directory over HTTP and opening `index.html`. PapaParse needs HTTP, not `file://`.
  ```
  python3 -m http.server 8000
  ```
- **Deploy** is `git push` to the branch GitHub Pages serves from.

## Conventions

- Vanilla JS, single HTML file, hand-written CSS — until/unless we deliberately choose otherwise.
- RTK chapter encoding in the data: integer chapter; `0` means kana-only words; `99` means contains non-RTK kanji.
- Kana-only rows are tagged with `kana_tier` (1–5) and `kind` (`vocab` | `morpheme` | `loanword`). `morpheme` rows must be filtered out of all user-facing display and CSV download. See FUTURE_PLANS.md for the migration record.
- `Heisig_numbers` in CSV rows is a stringified list (e.g. `[1, 2]`); strip brackets when displaying.
- Tone: friendly, concise, learner-focused. Match the voice already in [README.md](README.md) and the site copy.

## Designing learning features

Read [CHARTER.md](CHARTER.md) "Pedagogical foundation" before proposing or building anything that touches the learning experience.

- **Anchor each feature to a research-aligned principle.** Name which one it serves (spacing, retrieval practice, interleaving, dual coding, elaboration, desirable difficulties). Features without a clear principle need to make their case.
- **Every roadmap item in [FUTURE_PLANS.md](FUTURE_PLANS.md) must carry a one-line principle anchor** (or be tagged "UX correctness" / "infrastructure" if not pedagogical). When adding a new item, include the anchor at the time of writing — don't defer.
- **Watch the engagement-vs-acquisition reflex.** If a feature idea would feel at home on Duolingo (streaks, badges, daily-quota guilt, leaderboards), default no. We optimize acquisition, not engagement. See CHARTER.
- **Refuse pseudoscience.** Don't build for learning styles, left/right brain, subliminal acquisition, brain-training transfer claims. Full list in CHARTER.
- **Materials-first.** Any generative feature ships the inputs it uses (prompt templates, vocab slices, prompt-engineering rationale). Integrated experience + materials-only path coexist. See CHARTER.
- **Reading-side scope.** The optimization target is reading-side acquisition (visual recognition → functional reading + inner voice). Productive output (speaking, writing) is out of scope as a primary goal. Phonological access is acquired via vocabulary + audio, not per-kanji reading drills.

## Filter logic ("vocabulary the learner can read at chapter N")

The website's core filter — what counts as accessible vocabulary at a given RTK chapter — combines `Heisig_chapter`, `kana_tier`, and `kind`. As of the kana tier migration, the rule is:

**A row is accessible at user chapter `N` iff:**

```
if kind == "morpheme":     never accessible (always filtered out, regardless of N)
elif Heisig_chapter == 0:  accessible iff KANA_TIER_UNLOCKS[kana_tier] <= N
                           (kana_tier 1..5 → unlocks at chapter 0/1/10/25/40)
                           applies to kind "vocab" (hiragana) and kind "loanword" (katakana) alike
else:                      accessible iff Heisig_chapter <= N
                           (regular kanji rule)
```

Plus the user's frequency cutoff (`Frequency >= freqLimit`) applied uniformly.

Plus the optional "kanji-only" toggle, which excludes rows where `Heisig_chapter == 0` (kana) or `Heisig_chapter == 99` (non-RTK kanji).

Authoritative implementation lives in [index.html](index.html); `KANA_TIER_UNLOCKS` is the tunable constant. If the rule needs to change, update both this section and the code in the same commit so they don't drift.

## When in doubt

- Scope question ("does feature X belong here?") → check [CHARTER.md](CHARTER.md). If it's not clearly in or out, ask.
- Data question (regenerate? edit a CSV? change a column?) → ask before touching.
- Tech-stack question (add a framework? a backend? a build step?) → propose the smallest change that works and confirm before implementing.
