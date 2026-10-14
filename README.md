# book-translation (agent skill)

End-to-end pipeline for translating a whole book with real literary quality: OCR cleanup, glossary and rule sheet, chunked translation, three-lens agent review (voice / native craft / fidelity), final-editor merge, consistency pass, EPUB.

Born from translating a 40k-word Turkish novel into Russian; the pitfalls checklist is what actually went wrong there.

## Install

```sh
npx skills add <owner>/book-translation-skill            # interactive
npx skills add <owner>/book-translation-skill -g -a claude-code -y   # global, Claude Code, non-interactive
```

Or manually: copy `skills/book-translation/` into `~/.claude/skills/` (global) or `.claude/skills/` (project).

## Contents

- `skills/book-translation/SKILL.md` — the pipeline
- `skills/book-translation/templates/` — rule sheet, review brief, ready-to-paste agent prompts, final-editor rules
- `skills/book-translation/scripts/prepare_final.py` — buckets reviewer edits by chapter group (Python 3, stdlib only)

## Use

Ask your agent to "translate this book to <language> with the book-translation skill". Needs an agent that can spawn sub-agents for the review stages; `pandoc` for EPUB output.
