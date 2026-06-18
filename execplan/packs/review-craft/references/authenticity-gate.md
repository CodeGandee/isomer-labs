# Evidence Authenticity & Manuscript Coverage gate

The anti-fabrication core of review. Houmao's `evidence validate` only checks DB-row consistency
(supported-claims-without-support, open contradictions, orphans); this gate is the human/agent audit on
top of it that catches a polished-but-hollow or overclaimed paper. Run it before recommending `accept`.

## Build an experiment inventory
From logs, result rows, measurements, summaries, and the manuscript claims. For each experiment record:
- expected id / purpose
- **status from durable artifacts, not checklist labels**
- artifact paths; metrics actually present (open the files; do not trust ready-counts)
- current / stale / duplicate / failed / negative / superseded?
- does it appear in the manuscript (table/figure/caption)? which exact claim does it support?

**Recompute the real paper-facing result count manually** — do not trust ready counts when duplicate
rows, stale outline refs, pending rows, or missing metrics are present.

## Fabrication-risk labels (per result)
`no issue` · `provenance gap` · `manuscript overclaim` · `written-but-unsupported` · `contradiction` ·
`likely false or fabricated claim`.

## Gate verdict
A paper is NOT submission-ready unless ALL pass: compile/PDF, evidence provenance, manuscript coverage,
citation sufficiency, language hygiene, and experiment-matrix consistency. Map any failure to a route
(analysis / write / claim-downgrade / limitation), not to vague polishing.
