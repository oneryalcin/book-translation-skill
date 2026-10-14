---
name: book-translation
description: End-to-end pipeline for literary book translation with quality review (OCR cleanup, glossary, chunked translation, multi-lens agent review, final-editor merge, consistency pass, EPUB). Use when translating a whole book/novel or long text between languages and feel, voice and consistency matter.
---

# Literary book translation pipeline

Derived from translating a 40k-word Turkish novel to Russian. Priorities: the reader should feel the author's voice (not a literal rendering), names and terms stay consistent, and nothing is invented. Be honest that the result is a strong draft until a native reader has gone through it.

## 0. Intake (ask only what's unknown)
Source file/PDF, target language, intended use (private reading? publishing → copyright), voice-over/TTS needs (e.g. ё in Russian), any style preferences. Check copyright: author dead <70 yrs → private use only; say so once, user decides.

## 1. Clean the source
- PDF→MD: look for page-break paragraph splits (mid-word/mid-sentence), hyphenation, OCR casing (Turkish dotted/dotless i), comma↔period errors, stray symbols, repeated headers/page numbers.
- Script it: a Python (old,new) replacement list with uniqueness asserts; keep the original untouched, write `*.clean.md`. Never `sed -i` on macOS (use Python).
- Read the whole cleaned text once; doubts about a word → render that PDF page (`pdftotext` with spaces stripped to find the page, `pdftoppm -r 100`) and read the image.

## 2. Glossary & rules BEFORE translating
Write `glossary.md`: names (transliteration), nicknames (translate them), titles/honorifics policy, kept foreign/nautical/cultural terms (a short list), refrain/untranslatable chants (transliterate + one short translator's note supported by the source), quote marks, dialogue dash, special orthography (ё), proverb policy (target-language equivalents), forms of address, how to handle dialect speech, a tag policy for «he said».
Decide dialogue-tag policy now: source "said" verbs become calques; vary or drop tags; label-only lines get a verb; in a language with dative labels check speaker vs addressee.

## 3. Translate in chunks
Chapter-sized or ~10–15KB parts, each with the glossary, voice notes and last paragraphs for continuity. After each chunk: headings count, paragraph count vs source, no source-language letters. Concatenate with front matter; fix known OCR/idiom problems in a new file.

Judgement rules: render meaning and register, not words; idioms/proverbs → target idioms; humour and sound-play → recreate or note once; sensory images and rhythm (long breathless sentence then a snap) are the voice — protect them; never add explanations in the narrator's mouth.

## 4. Multi-lens editorial review (parallel agents)
Split the book into ~3 sections (~100–120KB each) with matching source sections. For each section run three agents on different models/lenses (voice/literary value, native craft/anti-translationese, fidelity vs source) using `templates/REVIEW_BRIEF.md`. Agents write OLD/NEW edit lists to files and never edit the book. Verify every OLD occurs exactly once.

## 5. Final-editor merge (do NOT apply edits mechanically)
Edits from three lenses overlap and conflict. Run `scripts/prepare_final.py RU.md TR.md OUT_DIR out_voice_*.md out_craft_*.md out_fidelity_*.md` to bucket proposals by chapter group, then run one strongest-model agent per group with `templates/FINAL_RULES.md` (adapt the glossary decisions). Output `G*_out.md`; each must keep paragraph count equal.
Assemble, then compare heading and paragraph counts with the draft.

## 6. Consistency pass
- Name-variant scan: capitalised tokens grouped by 5-letter stem with frequencies; fix drifting spellings.
- Quote/dash balance, double spaces, leftover source letters, leftover «he said» double tags, glossary terms.
- Read the whole book in order in ~55KB chunks; fix only real faults (register slips, nonsense, term drift). Ask about source-problem passages by checking the PDF page image; keep the author's own errors and flag them.

## 7. Deliver
- Plain `.md` and `.epub`: `pandoc book.md -t epub3 -o out.epub --toc --toc-depth=2 --split-level=2 --css style.css --metadata title=… --metadata author=… --metadata lang=…` (strip duplicate H1 from the body; verify nav lists every chapter).
- Final message: location, stats, conventions, judgement calls, honest caveats, offer a polish pass or a short sample for a native reader.

## Templates in this skill
- `templates/GLOSSARY_TEMPLATE.md` — rule sheet / glossary to fill before step 3 and paste into every prompt.
- `templates/REVIEW_BRIEF.md` — shared brief + strict OLD/NEW edit format for the three lens reviewers (step 4).
- `templates/AGENT_PROMPTS.md` — ready-to-paste prompts: chunk translator, voice, craft, fidelity reviewers, final editor, consistency reader.
- `templates/FINAL_RULES.md` — final-editor rule sheet (step 5).
- `scripts/prepare_final.py` — buckets reviewer edits by chapter group (step 5).

## Pitfalls checklist
dative speaker labels; dropped pronouns changing gender/number; literal idioms; place names mistaken for nouns; multi-speaker passages collapsed into one quote; translator parentheses in text; invented etymologies in notes; reviewers' false "mistranslation" claims (verify); authors' typos/arithmetic (keep, flag); transliteration drift; inconsistent hyphenated-title declension; sharecropper/tenant-type term drift.
