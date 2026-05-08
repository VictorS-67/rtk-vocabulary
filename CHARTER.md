# RTK Companion — Charter

The "why" of this project. For "how to work here," see [CLAUDE.md](CLAUDE.md). For user-facing intro and dataset details, see [README.md](README.md).

## Mission

Help learners of *Remembering the Kanji* (RTK, 6th edition) practice with material they can actually read at their current chapter — and grow, over time, into a broader companion toolkit around the RTK journey.

## Audience

Independent learners working through *Remembering the Kanji* by James W. Heisig. Self-directed, motivated, comfortable with a single-page web tool or a CSV download. Not absolute beginners to Japanese; not learners using a non-RTK method to acquire kanji.

## What this project IS

- A vocabulary filter that maps known RTK kanji → words a learner can read at their level.
- A small set of curated, frequency-ranked datasets that pair Japanese vocabulary with the RTK chapter required to read it.
- A starting point for an integrated RTK companion toolkit — features beyond vocab filtering (e.g., short stories composed only of known kanji, reading practice, exports to SRS tools, quizzes) are welcome when they fit the mission.

## Vision (longer term)

Begin as an RTK companion toolkit. Architect decisions so future expansion toward a broader Japanese learning hub — for RTK-aware learners — is not painted into a corner. RTK progression stays the organizing principle even as the scope grows; we don't drift into "general Japanese learning site with no anchor."

## What this looks like for learners

Concrete user journeys at representative chapter levels — to make the abstract scope tangible. The journeys evolve as roadmap features land; current state reflects what's available today (vocab filter + CSV download) plus what's intended near-term.

### Just starting — RTK chapter ~5

Has learned ~150 kanji. Opens the site at chapter 5: sees a small grid of words they can already read — kana scaffolding (tier 1 + early tier 2) plus simple kanji words like 一日, 人口, 山. Maybe 30–80 words depending on the frequency cutoff. Downloads the CSV, hands it to an LLM with the prompt: *"write a very simple Japanese paragraph using only these words."* Gets back something like *"私は山に行く。山は大きい。"* — readable, theirs. Practice reading it aloud (with planned audio feature) builds the inner-voice / phonological link.

### Mid-RTK — chapter ~25

Has learned ~700 kanji. The vocab grid now shows hundreds of words; tier 3 kana is unlocked. Stories from an LLM are paragraph-length, modest narrative. Starts using the (planned) Anki export to add new kanji-words to their own SRS. Toggling furigana off (planned) for known words is now a real self-test.

### Deep RTK — chapter ~50

Has learned ~1800 kanji. The vocab CSV is rich enough for daily news, casual content. Stories can be sophisticated. Sample sentences (planned) are no longer simplistic. Phonological access via audio is well-established for high-frequency words. Project's role shifts toward "vocab confidence + reading-practice booster" as the learner starts approaching native content.

### Post-RTK

Has all 2200+ kanji. No chapter restriction; the project becomes a curated dictionary + reading-practice tool. Audio + sample sentences for words they recognize but don't yet "own." Useful as a long-term consolidation companion while transitioning to native input (manga, news, novels).

## Pedagogical foundation

We adopt **Remembering the Kanji** as our kanji-recognition foundation. We do not claim it is empirically the only valid path — credible alternatives exist (WaniKani, vocabulary-first methods, traditional school curricula). What we claim is that for learners who *have chosen RTK*, the integrated learning system that the book itself does not provide is what we build.

### Optimization target

Bridge from RTK-style visual recognition to **functional reading at the learner's level**, including phonological access (the "inner voice" while reading). Reading-side, receptive acquisition.

Out of scope as primary goals: generic "Japanese mastery"; productive output skills (speaking, writing) — those need different practice modalities we don't currently address.

Phonological access is acquired through **vocabulary + audio exposure in context**, not through explicit per-kanji reading drills. Skilled readers retrieve word-level pronunciations directly from the visual form (Coltheart, Perfetti, Seidenberg & McClelland); sub-lexical reading is a fallback. Optimizing the dominant pathway means vocabulary-level audio-text pairing.

### Research-aligned principles

When designing or evaluating a learning feature, anchor it to specific evidence-supported principles from cognitive psychology and education research:

- **Spacing effect** — distributed > massed practice
- **Retrieval practice / testing effect** — self-testing > re-reading
- **Interleaving** — mixed > blocked practice for long-term retention
- **Desirable difficulties** (Bjork) — making encoding slightly harder helps later recall
- **Dual coding** (Paivio) — pairing verbal + visual encoding aids memory
- **Elaboration** — connecting new material to existing knowledge

Features that don't ground in at least one of these (or another well-supported principle) need to make their case explicitly.

### Engagement-vs-acquisition

We optimize for **acquisition**, not engagement. Streak mechanics, daily-quota gamification, and other engagement-bait patterns that ed-tech defaults to are out of scope — research shows they can actively undermine deep learning by reinforcing surface performance. The no-monetization stance frees us from the incentive to build them.

### Pseudoscience refusals

We do not build features that depend on:

- **Learning styles** (visual / auditory / kinesthetic preference matching) — robustly debunked
- **Right-brain / left-brain** framings
- **Sleep learning / subliminal acquisition** — no meaningful effect
- **Brain-training transfer claims** — most don't generalize beyond the trained task
- **Strict input-only theories** that prohibit explicit instruction or output practice as a matter of principle

## What this project is NOT (firm non-goals)

- **Not a kanji-learning tool.** It presupposes the learner is using RTK (or another method) to learn kanji. We don't teach kanji from scratch and we don't replace the book.
- **Not a general dictionary.** Vocabulary is curated by RTK progression and frequency. For arbitrary word lookup, learners should use Jisho or similar.
- **Not a productive-skills trainer.** Speaking and writing practice need feedback loops, conversation partners, and modalities outside our scope.
- **Not engagement-driven.** No streaks, no daily-quota guilt, no gamification for its own sake. See "Engagement-vs-acquisition" above.

## Current stances (revisable, but deliberate)

These are not firm non-goals — they're the project's current posture. Changing them should be a deliberate decision, not a drift.

- **Static, runs in the browser.** No accounts, no server-side state. A backend may be introduced if a future feature genuinely requires it (e.g., LLM-generated content caching, cross-device progress sync). Easily reversible — start static, switch if justified.
- **Free and open, no monetization.** No paywalls, no ads, no premium tiers. Donations or tips are compatible with this stance. Reversing this is technically easy but socially costly once an audience exists; preserve the stance unless there's a strong reason to change it.
- **Datasets are hand-curated artifacts, not pipeline output.** No data-collection or regeneration scripts live in this repo today. Bringing the pipeline in-repo (likely under `data/pipeline/` or `tools/`) becomes worthwhile when one of these is real: (a) a second corpus is added, (b) the existing dataset needs a refresh, or (c) a new column is needed across rows. Until then, building the pipeline speculatively is YAGNI; the current CSVs are the source of truth.

## Operating principles

- **Runs in the browser by default.** Anyone can fork, host, and run. GitHub Pages is the canonical deployment.
- **Datasets are inputs, not outputs.** They were hand-curated once; the website consumes them. Treat them as load-bearing data files, not as things to regenerate casually.
- **RTK progression is the organizing axis.** Every feature should answer: "how does this serve someone at chapter N of RTK?"
- **Materials-first / personalization.** Generative features (story prompts, sentence prompts, image prompts, etc.) ship the prompt templates, vocabulary slices, and any other inputs they use. The integrated experience and the materials-only path coexist: integrated path serves the median learner; materials let power users replicate, adapt, and personalize. Both belong to the public-resource mission. AI access keeps commoditizing — locking value into "our service that you can't replicate" creates pointless lock-in and dates badly.
- **Friendly, learner-focused tone.** Match the voice in [README.md](README.md) and the site copy.
- **MIT for code, CC BY 4.0 for data.** See [LICENSE](LICENSE) (code) and [LICENSE-DATA](LICENSE-DATA) (datasets).
- **Not affiliated with James Heisig or the RTK publisher.** Chapter and frame numbers are factual references.
