# Pack: nature-data

- kind: template
- backs: manuscript datastmt
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- entrypoint: `adapter:generate`
- input: data-inventory JSON
- output: .md Data Availability statement + citations + FAIR checklist
- example input: examples/inventory.json (never invents DOIs/accessions)
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## DA-statement methodology
`references/statement-patterns.md` (11 templates + anti-patterns), `fair-metadata-checklist.md`, `repository-and-identifiers.md`. Avoid the 'available on request' anti-pattern; never invent identifiers. Also: `chinese-author-alignment.md` (CN→EN data-availability wording; relevant to bilingual output). Also: `source-basis.md` (primary-source policy map: Springer Nature / Nature Portfolio / Scientific Data / FAIR / DataCite — for auditing why each rule exists).
