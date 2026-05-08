"""
Kana tier migration: adds `kana_tier` and `kind` columns to
jp_freq_translation_reading.csv and adds a few missing rows.

Run from the repo root:
    python3 tools/migrate_kana_tiers.py

Reads / writes (in place, idempotent):
  - jp_freq_translation_reading.csv

Logic:
  - Non-chapter-0 rows: kana_tier=blank, kind=vocab
  - Chapter-0 rows:
      * If word is in TIER1 → tier 1, kind=vocab
      * Elif TIER2 → tier 2, kind=vocab
      * Elif word is in MORPHEMES → kind=morpheme, tier=blank
      * Elif word is all katakana → kind=loanword, tier by frequency rank
      * Else → kind=vocab, tier by frequency rank (3, 4, or 5)
  - Tier 3-5 boundaries: configurable below; tuned for vocab and loanword separately.
  - Three corpus gaps appended as tier 2 vocab: あんな, それなら, ください.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "jp_freq_translation_reading.csv"
DELIM = ";"

# --- Curated tier 1: structurally indispensable kana ---
# Words a Japanese sentence essentially needs regardless of vocabulary level.
TIER1 = frozenset([
    # Particles
    "は", "が", "を", "に", "で", "と", "も", "の", "へ", "から",
    "まで", "や", "か", "よ", "ね",
    # Copula & existence
    "です", "だ", "ある", "いる", "ない",
    # Core verbs typically written in kana
    "する", "なる", "できる", "いう",
    # こそあど demonstratives
    "これ", "それ", "あれ", "どれ",
    "この", "その", "あの", "どの",
    "ここ", "そこ", "あそこ", "どこ",
    "こう", "そう", "ああ", "どう",
    # Question words
    "いつ", "なぜ", "どうして", "いくつ",
    # Connectives
    "でも", "それから", "だから", "のに", "ので",
    # Scope / quantifier particles
    "だけ", "しか", "ぐらい", "ばかり",
    # High-frequency adverbs
    "とても", "もう", "まだ", "ちょっと",
    # High-frequency core that turned out to be very common in the corpus
    "よう", "という", "さん", "けど", "あと", "もっと", "みんな",
    "なに", "なん", "わたし",
])

# --- Curated tier 2: hand-picked second band of essentials ---
# Common everyday words still mostly hiragana; expands the LLM's natural
# vocabulary at chapter 1+. (Top katakana also flow into tier 2 by frequency
# rank, see TIER_BOUNDARIES below.)
TIER2 = frozenset([
    # Adverbs
    "たくさん", "いつも", "よく", "たぶん", "やはり", "やっぱり",
    "ほとんど", "すぐ", "もちろん", "きっと", "なかなか", "だんだん",
    "どんどん", "ずっと", "ぜんぜん", "たまに", "ゆっくり", "はっきり",
    "なるべく", "そろそろ", "なんとか", "どうしても", "まるで", "けっして",
    "ちっとも", "ちょうど", "せっかく", "おそらく", "もしかして", "もし",
    "やがて", "ぴったり", "やっと",
    # こそあど extended
    "こんな", "そんな", "あんな", "どんな",
    "こっち", "そっち", "あっち", "どっち",
    "こちら", "そちら", "あちら", "どちら",
    # Connectives
    "それで", "それでも", "それなら", "すると", "ところが", "ところで",
    "けれど", "しかし", "つまり", "ただ", "たとえば",
    "そして", "また", "まず",
    # Phrases / interjections / common adjectives
    "ください", "ありがとう", "すみません", "ごめん", "はい", "いいえ",
    "ぜひ", "いい", "すごい", "だめ", "どうも", "なるほど",
    # Abstract / formal nouns
    "もの", "こと", "とき", "ところ", "ため", "ほう", "はず", "みたい",
    "ほか", "まま", "わけ", "うち", "ほど", "つもり", "かわり", "など",
    # Common kana verbs
    "もらう", "くれる", "あげる", "やる", "しまう", "おく",
    # Common kana adjectives
    "かわいい", "きれい", "やさしい", "うれしい", "さびしい",
    # Verbs from data audit (often kana in this corpus)
    "くる", "いく", "みる", "おる", "ござる", "ほしい",
    # Suffixes / contractions / common words from data audit
    "ちゃん", "かも", "いろいろ", "すべて", "まったく", "すでに",
    "とにかく", "とりあえず", "だって", "いっぱい",
    "てる", "ちゃう", "ぼく", "せい",
])

# --- Morphemes to exclude from any tier ---
# Conjugational/grammatical morphemes the Leeds tagger surfaced as standalone
# entries but which are not "vocabulary words" a learner looks up. They get
# kind=morpheme and tier=blank; the website filters them out.
MORPHEMES = {
    # Verb conjugation auxiliaries
    "て", "た", "ます", "ました", "ません",
    "れる", "られる", "せる", "させる",
    "たい", "ない",  # NOTE: ない also has standalone vocab use; tier list overrides
    "ながら", "たり", "つつ",
    "ぬ", "う", "ば", "なら", "たら",
    "ん", "まい", "たがる",  # contraction, neg-volitional, 3p-desiderative
    # Honorific prefixes
    "お", "ご",
    # Inflection/fragment artifacts (single-char hiragana that aren't real words)
    "く", "ら", "ろ", "ども", "べし",
    "ま", "す", "り", "つ", "い", "こ", "ど", "る",
    "き", "じ", "ぜ", "ぴ", "ふ", "ぶ",
    # Sentence-ending fragments / interjections that aren't really vocab
    "なぁ", "なあ", "ちゃ", "ちゃう", "ちゃん",  # ちゃう/ちゃん handled via tier list override
    "って", "じゃ",
    "なお", "なり",
    # Single-char katakana (almost always tagger fragments, not standalone words)
    "ン", "ク", "ラ", "リ", "ド", "レ", "ロ", "シ", "ソ", "パ", "ノ",
    "ル", "ス", "タ", "テ", "ト", "ハ", "バ", "ピ", "プ", "ペ", "ポ",
    "マ", "ミ", "ム", "メ", "モ", "ヤ", "ユ", "ヨ", "ワ", "ヲ",
    "ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ケ", "コ",
    "サ", "セ", "チ", "ツ", "ニ", "ヌ", "ネ", "ヒ", "ヘ", "ホ",
    "ナ", "ジ", "ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ズ", "ゼ", "ゾ",
    "ダ", "ヂ", "ヅ", "デ", "ビ", "ブ", "ベ", "ボ", "ャ", "ュ", "ョ",
    "ラ", "ー",
}

# A few words from the preliminary tier list override morpheme tagging.
# (e.g., ちゃん is a real honorific suffix, ちゃう is vocab-relevant contraction)
# These get whatever the preliminary list says.

# --- Tier boundaries (by rank within each kind) ---
# Tier 3-5 are derived from frequency rank among the *residual* chapter-0
# rows of each kind (vocab not in tier 1/2 preliminary; loanwords).
TIER_BOUNDARIES = {
    "vocab":    {3: 300, 4: 800},   # tier 3 = ranks 1-300; tier 4 = 301-800; tier 5 = 801+
    "loanword": {2:  50, 3: 250, 4: 750},  # tier 2 = top 50; tier 3 = 51-250; tier 4 = 251-750; tier 5 = 751+
}

# --- Missing rows to add ---
# Tier matches their assignment in kana_tiers_preliminary.csv:
# - あんな is tier 2 (consistent with こんな/そんな/どんな at tier 2)
# - それなら is tier 2 (complex connective)
# - ください is tier 2 (phrase)
NEW_ROWS = [
    # word, frequency, reading, english, tier
    ("あんな", "0.01", "あんな", "that kind of (yonder)", "2"),
    ("それなら", "0.01", "それなら", "if so / in that case", "2"),
    ("ください", "0.01", "ください", "please give / please do", "2"),
]


def is_all_katakana(word: str) -> bool:
    """True if every char is in the katakana block (incl. long-vowel mark)."""
    if not word:
        return False
    for c in word:
        if not ("゠" <= c <= "ヿ"):
            return False
    return True


def is_all_hiragana(word: str) -> bool:
    if not word:
        return False
    for c in word:
        # Allow long-vowel mark in hiragana words too (e.g., なー, あー)
        if not (("぀" <= c <= "ゟ") or c == "ー"):
            return False
    return True


def main():
    tier1_set, tier2_set = TIER1, TIER2
    print(f"Embedded tier lists: tier 1 = {len(tier1_set)}, tier 2 = {len(tier2_set)}", file=sys.stderr)

    # Read source
    with SRC.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=DELIM)
        rows = list(reader)
        original_fields = list(reader.fieldnames)

    # Make idempotent: drop the migration's own columns if present and any
    # rows previously added by this script (identified by Frequency == "0.01"
    # and Heisig_chapter == "0" matching one of the NEW_ROWS words).
    base_fields = [f for f in original_fields if f not in ("kana_tier", "kind")]
    new_words = {w for (w, *_) in NEW_ROWS}
    rows = [
        r for r in rows
        if not (r["Heisig_chapter"] == "0" and r["Word"] in new_words and r["Frequency"] == "0.01")
    ]
    for r in rows:
        r.pop("kana_tier", None)
        r.pop("kind", None)

    print(f"Read {len(rows)} rows from {SRC.name} (after idempotency cleanup)", file=sys.stderr)

    # First pass: classify and assign known tiers; collect residuals for ranked tiering
    residual_vocab = []     # rows needing tier 3/4/5 by frequency rank (hiragana vocab)
    residual_loanword = []  # rows needing tier 2/3/4/5 by frequency rank (katakana)

    for row in rows:
        ch = row["Heisig_chapter"]
        word = row["Word"]

        # Defaults for non-chapter-0 rows (kanji vocab)
        if ch != "0":
            row["kana_tier"] = ""
            row["kind"] = "vocab"
            continue

        # Chapter-0 classification
        if word in tier1_set:
            row["kana_tier"] = "1"
            row["kind"] = "vocab"
        elif word in tier2_set:
            row["kana_tier"] = "2"
            row["kind"] = "vocab"
        elif word in MORPHEMES:
            row["kana_tier"] = ""
            row["kind"] = "morpheme"
        elif is_all_katakana(word):
            row["kana_tier"] = ""  # filled in second pass
            row["kind"] = "loanword"
            residual_loanword.append(row)
        else:
            row["kana_tier"] = ""  # filled in second pass
            row["kind"] = "vocab"
            residual_vocab.append(row)

    # Second pass: assign tier 3/4/5 (and tier 2 for loanwords) by frequency rank
    def assign_by_rank(rows_list, boundaries):
        sorted_rows = sorted(rows_list, key=lambda r: float(r["Frequency"]), reverse=True)
        thresholds = sorted(boundaries.items())  # [(tier, max_rank), ...] sorted by tier
        for rank, row in enumerate(sorted_rows, start=1):
            assigned = None
            for tier, max_rank in thresholds:
                if rank <= max_rank:
                    assigned = tier
                    break
            if assigned is None:
                # Fall through to last tier
                assigned = max(thresholds, key=lambda x: x[0])[0] + 1
            row["kana_tier"] = str(assigned)

    assign_by_rank(residual_vocab, TIER_BOUNDARIES["vocab"])
    assign_by_rank(residual_loanword, TIER_BOUNDARIES["loanword"])

    # Add the three missing rows (as new entries at end with new ids)
    next_id = max(int(r["id"]) for r in rows if r["id"].isdigit()) + 1
    for word, freq, reading, english, tier in NEW_ROWS:
        rows.append({
            "id": str(next_id),
            "Word": word,
            "Frequency": freq,
            "Reading": reading,
            "English": english,
            "Heisig_numbers": "[]",
            "Heisig_chapter": "0",
            "kana_tier": tier,
            "kind": "vocab",
        })
        next_id += 1

    # Stats
    tier_counts = {}
    kind_counts = {}
    for row in rows:
        if row["Heisig_chapter"] == "0":
            t = row["kana_tier"] or "(none)"
            k = row["kind"]
            tier_counts[t] = tier_counts.get(t, 0) + 1
            kind_counts[k] = kind_counts.get(k, 0) + 1
    print("=== Chapter-0 distribution after migration ===", file=sys.stderr)
    print("By kana_tier:", file=sys.stderr)
    for t in sorted(tier_counts.keys()):
        print(f"  tier {t}: {tier_counts[t]}", file=sys.stderr)
    print("By kind:", file=sys.stderr)
    for k in sorted(kind_counts.keys()):
        print(f"  {k}: {kind_counts[k]}", file=sys.stderr)

    # Write output
    new_fields = base_fields + ["kana_tier", "kind"]
    with SRC.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields, delimiter=DELIM, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} rows to {SRC.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
