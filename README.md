# RTK Vocabulary Project

This repository links frequently used Japanese vocabulary to the kanji order in *Remembering the Kanji* (RTK) by James W. Heisig (6th edition).

It allows learners to find vocabulary that they can read based on their progress in the book.

## 🌐 Web Interface

A web-based tool is available to easily filter and download vocabulary lists:

👉 **[Launch RTK Vocabulary Filter](https://victors-67.github.io/rtk-vocabulary/)**

### How it works
1. **Enter your progress**: Input the last chapter of *Remembering the Kanji* you have completed.
2. **Filter**: The tool processes the vocabulary list to find words composed ONLY of keywords you have learned (or words written in Kana).
3. **Download**: Get a CSV file containing your personalized vocabulary list.

The website runs entirely in your browser using the `jp_freq_translation_reading.csv` dataset.

---

## 📂 Datasets

This repository contains processed CSV datasets that map vocabulary to Heisig chapters.

### 1. General Vocabulary (`jp_freq_translation_reading.csv`)
*Used by the website.*
Contains general Japanese words, including particles and common terms.
- **Source**: [Leeds Corpus](https://www.manythings.org/japanese/words/leeds/) (Internet-jp frequency).
- **Columns**:
  - `Word`: The Japanese word.
  - `Frequency`: Frequency score from the corpus.
  - `Reading`: Hiragana/Katakana reading.
  - `English`: English translation or grammatical function.
  - `Heisig_numbers`: List of RTK numbers for kanji in the word (9999 for non-RTK kanji).
  - `Heisig_chapter`: The RTK chapter required to know all kanji in the word.

### 2. Heisig Index (`heisig_kanjis.csv`)
A reference list of all kanji in the book.
- **Columns**:
  - `Kanji`: The character.
  - `Heisig_number`: Its index in the book.
  - `Chapter`: The chapter it appears in.

### 3. Jukugo (Compound Words) (`jokugos_freq_db_heisig_hiragana.csv`)
A dataset focusing specifically on two-kanji compound words (Jukugo).
- **Source**: Derived from news content frequency.
- **Columns**:
  - `Composite_word`: The 2-kanji word.
  - `Frequency`: Frequency in news articles.
  - `Grammatical_feature`: Part of speech (e.g., noun, adverb).
  - `Pronunciation`: Reading in Hiragana.
  - `English Translation`: Meaning.
  - `Heisig_numbers`: List of RTK numbers.
  - `Heisig_chapter`: The RTK chapter required to know the word.
