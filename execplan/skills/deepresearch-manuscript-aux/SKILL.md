---
name: deepresearch-manuscript-aux
description: "Use when a writer needs venue-style English polishing of a manuscript or a Data-Availability statement drafted from a manuscript/data inventory. Triggers — \"polish the manuscript English\", \"polish to Nature style\", \"write the data-availability statement\". Tools `manuscript polish` (nature-polishing) and `manuscript datastmt` (nature-data). Style/structure only; additive artifacts; never adds unsupported claims, never invents DOIs/accessions. Quest-isolated. Roles: writer."
---

# deepresearch-manuscript-aux (prose / data helpers)

## Overview
Two `$HARNESS`-backed helpers for the manuscript stage: `polish` rewrites manuscript English to a venue style (style only), and `datastmt` drafts a Data-Availability statement from a verified data inventory. Both emit additive report artifacts and never introduce or strengthen scientific claims.

## When to Use
- The writer asks to "polish the manuscript English" or "polish to Nature style" → run the `polish` action.
- The writer asks to "write the data-availability statement" → run the `datastmt` action.
- You are operating as the **writer** role inside a single quest, typically during the optional venue-passes step after the manuscript prose exists.

When NOT to use:
- For drafting/rewriting manuscript prose, building or validating the outline, or shaping how evidence reads — that is `deepresearch-paper-craft` methodology, not these mechanical passes.
- For compiling the manuscript to PDF use `deepresearch-paper-latex`; for figures use `deepresearch-figure`.
- Do not use to add, strengthen, or invent claims, citations, DOIs, or accessions — these actions are additive and substance-preserving only.
- Do not cross quest boundaries: every action runs against a single `<q>` and reads/writes only that quest's artifacts.

## Workflow
1. Identify the action from the request: English polishing → `polish`; data-availability statement → `datastmt`.
2. Confirm the required inputs exist for that quest (see Commands): for `polish`, the source manuscript `runs/<q>/report/paper.md`; for `datastmt`, the verified data inventory `<inventory.json>`.
3. Run the matching `$HARNESS` command verbatim, substituting `<q>` (quest id), `<role>` (your role, normally `writer`), and the input path. Keep the `--via skill:...` audit stamp exactly as written.
4. Verify the additive artifact was written to its `--ref` path and recorded under its `--artifact-id`. The action only adds a new artifact; it never overwrites the source manuscript or inventory.
5. Hand the resulting artifact back through the normal task-result path so it flows into the manuscript pipeline.
6. If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Commands
Substitute `<q>` (quest id) and `<role>` (your role). Preserve the `--via skill:...` stamp verbatim so the exact runtime-adapter identity is preserved in the audit.

`polish` — nature-polishing → venue English polishing (style only):
```
$HARNESS --via skill:deepresearch-manuscript-aux/polish:<role> manuscript polish --quest-id <q> \
  --artifact-id <q>:polished --ref runs/<q>/report/paper-polished.md --input runs/<q>/report/paper.md
```
Style only; flags overclaim terms as suggestions; never strengthens or adds claims.

`datastmt` — nature-data → Data-Availability statement:
```
$HARNESS --via skill:deepresearch-manuscript-aux/datastmt:<role> manuscript datastmt --quest-id <q> \
  --artifact-id <q>:datastmt --ref runs/<q>/report/data-availability.md --input <inventory.json>
```
Drafts only from the verified data inventory; never invents DOIs/accessions; avoids "available on request".

## Common Mistakes
- Strengthening or adding claims during `polish`. It is style only — surface overclaim terms as suggestions, never rewrite the science.
- Inventing DOIs or accessions, or falling back to "available on request" in `datastmt`. Draft only from the verified inventory; if a datum is absent from the inventory, it is absent from the statement.
- Overwriting the source. These are additive artifacts (`paper-polished.md`, `data-availability.md`) under distinct `--artifact-id`s; never edit `paper.md` or the inventory in place.
- Dropping or rewriting the `--via skill:deepresearch-manuscript-aux/<action>:<role>` stamp. The exact stamp must be preserved so the runtime-adapter identity is auditable.
- Confusing these mechanical passes with `deepresearch-paper-craft` outline/write methodology, or trying to compile a PDF here.
- Crossing quest isolation by reading another quest's manuscript or inventory.

## Audit / Boundaries
- Invoke as `--via skill:deepresearch-manuscript-aux/<action>:<role>` so the exact runtime-adapter identity is preserved in the audit.
- Additive report artifacts only; style/structure only — never adds unsupported claims, never invents DOIs. Quest-isolated.

## Red Flags — never rationalize away
| Rationalization | Reality |
| --- | --- |
| "This sentence reads weak; I'll firm up the claim while polishing." | `polish` is style only. Strengthening a claim is out of scope — flag it as a suggestion at most. |
| "The inventory is missing the DOI; I'll fill in a plausible one." | Never invent DOIs/accessions. Draft only from verified inventory entries. |
| "No accession yet, I'll write 'data available on request'." | `datastmt` must avoid "available on request"; state only what the inventory verifies. |
| "I'll just edit paper.md directly instead of a new artifact." | Artifacts are additive; the source manuscript and inventory are never overwritten. |
| "I can reuse another quest's data-availability statement." | Quest-isolated — read and write only the current quest's artifacts. |
