# RTK Companion

An open, science-aligned learning toolkit for people working through *Remembering the Kanji* (RTK) by James W. Heisig.

RTK teaches you to recognize and assign meaning to ~2200 kanji. It does not teach you readings, vocabulary, or how to actually read Japanese text. **RTK Companion is the integrated system that fills that gap** — starting with vocabulary at your current chapter, growing toward sample sentences, audio, and reading practice paced to your level.

## 🌐 Web Interface

A web-based tool is available to filter and download vocabulary at your level:

👉 **[Launch the RTK Companion vocabulary filter](https://victors-67.github.io/rtk-companion/)**

### How it works

1. **Enter your progress.** Input the last RTK chapter you have completed.
2. **Filter.** The tool returns words you can read at that chapter — every kanji in the word is one you've learned, and any kana in the word is at a tier appropriate for your level. Optionally cap by frequency or restrict to RTK kanji.
3. **Download.** Get a CSV of your personalized vocabulary list. Hand it to your favorite LLM with a prompt like *"write a Japanese paragraph using only these words"* for instant level-paced reading practice.

The website runs entirely in your browser using the `jp_freq_translation_reading.csv` dataset. **No accounts, no analytics, no data leaves your machine.** Your filter inputs are not stored or transmitted anywhere.

---

## 📂 Datasets

Processed CSV datasets that map vocabulary to Heisig chapters.

### 1. General Vocabulary (`jp_freq_translation_reading.csv`)

*Used by the website.* Contains general Japanese words, including particles, common kana words, and katakana loanwords.

- **Source**: [Leeds Corpus](https://www.manythings.org/japanese/words/leeds/) (internet-jp frequency).
- **Columns**:
  - `Word`: the Japanese word
  - `Frequency`: frequency score from the corpus
  - `Reading`: hiragana/katakana reading
  - `English`: English translation or grammatical function
  - `Heisig_numbers`: list of RTK numbers for kanji in the word (9999 for non-RTK kanji)
  - `Heisig_chapter`: the RTK chapter required to know all kanji in the word (`0` for kana-only words; `99` for words containing non-RTK kanji)
  - `kana_tier` *(added by the kana tier migration)*: integer 1–5 for kana-only rows, blank for kanji rows. Lower tier = more essential / unlocks earlier. Drives the progressive unlocking of kana words alongside RTK chapter progress.
  - `kind` *(added by the kana tier migration)*: `vocab` | `morpheme` | `loanword`. `morpheme` rows are grammatical morphemes the corpus tagged as standalone words (て, た, ます, …) and are filtered out of all user-facing display and CSV download.

### 2. Heisig Index (`heisig_kanjis.csv`)

A reference list of all kanji in the book.

- **Columns**: `Kanji`, `Heisig_number`, `Chapter`.

### 3. Jukugo (Compound Words) (`jokugos_freq_db_heisig_hiragana.csv`)

A dataset focusing on two-kanji compound words. Not currently consumed by the website — kept as a downloadable reference.

- **Source**: derived from news content frequency.
- **Columns**: `Composite_word`, `Frequency`, `Grammatical_feature`, `Pronunciation`, `English Translation`, `Heisig_numbers`, `Heisig_chapter`.

---

## 🧭 Project documentation

Internal docs explaining how the project is built and where it's going. Public for transparency:

- [CHARTER.md](CHARTER.md) — mission, audience, pedagogical foundation, non-goals
- [FUTURE_PLANS.md](FUTURE_PLANS.md) — roadmap and decision log
- [CLAUDE.md](CLAUDE.md) — conventions for working in this repo (and for AI collaborators)

The pedagogical stance is explicit: optimize for **acquisition** (research-aligned principles like spacing, retrieval practice, dual coding, elaboration), **not engagement** (no streaks, badges, or daily-quota gamification). See [CHARTER.md](CHARTER.md) for the full pedagogical foundation.

---

## License & Credits

### The Code

The source code for this website (HTML, JavaScript, CSS, Python tooling) is licensed under the **MIT License**. See [LICENSE](LICENSE).

### The Data

The CSV datasets are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. See [LICENSE-DATA](LICENSE-DATA) for the full notice and attribution chain.

The main dataset (`jp_freq_translation_reading.csv`) is a derivative work based on the **Leeds Archive of Japanese Words** via [Manythings.org](https://www.manythings.org/japanese/words/leeds/).

- **Original Data Source:** distributed under the [Creative Commons Attribution 2.5 Generic License (CC BY 2.5)](https://creativecommons.org/licenses/by/2.5/).
- **Modifications:** English translations, Heisig (RTK) index numbers, and the `kana_tier` / `kind` columns were added to the original frequency list.
- **Heisig / RTK reference:** the Heisig chapter and frame numbers are factual references to the book *Remembering the Kanji* by James Heisig. This project is not affiliated with, nor endorsed by, James Heisig or the publisher.
