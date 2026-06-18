---
name: deepresearch-manuscript-aux
description: Polishes manuscript English to venue style or drafts a Data-Availability statement from an existing manuscript/inventory, routing to one of two template-pack-backed actions — polish (style-only English) or datastmt (Data-Availability statement). Use when the writer needs venue-style prose polishing or a data-availability statement. Emits additive artifacts only; never adds unsupported claims and never invents DOIs/accessions.
---

# manuscript-aux (prose / data helpers)

Trigger: "polish the manuscript English / to Nature style", or "write the data-availability statement".

## actions
- `polish`   → `manuscript polish`   (nature-polishing) — venue English polishing (style only). See actions/polish.md.
- `datastmt` → `manuscript datastmt` (nature-data)      — Data-Availability statement. See actions/datastmt.md.

## audit / boundaries
- Invoke as `--via skill:deepresearch-manuscript-aux/<action>:<role>` so the exact pack identity is preserved in the audit.
- Additive report artifacts only; style/structure only — never adds unsupported claims, never invents DOIs. Quest-isolated.
