# Pack: nature-polishing

- kind: template
- backs: manuscript polish
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- entrypoint: `adapter:generate`
- input: text/Markdown manuscript prose
- output: .md polished prose + editor-notes (style only; no claims changed)
- example input: examples/draft.md
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## Style methodology
`references/style-guardrails.md` (incl. the overclaim checklist), `section-moves.md`, `phrasebank-playbook.md`, `writing-strategy.md`. The adapter flags overclaim terms as suggestions; it never strengthens a claim.
