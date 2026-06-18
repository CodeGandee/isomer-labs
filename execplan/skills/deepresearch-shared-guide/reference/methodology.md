# Methodology references and usage audit (all roles)

This is the depth behind the "Research-quality disciplines" section of `SKILL.md`. Read the relevant part
before stage work.

## Methodology references

These are loop-wide research/writing **craft** packs (`kind='reference'`, enabled by default). Discover with
`$HARNESS knowledge query --kind reference` and list their files with `$HARNESS knowledge cards`; then READ
the named file under `execplan/packs/<pack>/references/...`. They are advisory craft, NEVER an authoritative
state surface (the DB stays canonical; record outcomes via `record apply`). Map any external tool names
inside them (`artifact.*`, `bash_exec`, `memory.*`) to the `$HARNESS` surface.

- `ideation-rubric` — objective contract, selection gate, divergence/related-work playbooks, eval-contract + baseline-shortlist (scope/idea).
- `research-method` — evidence ladder, comparability contract, campaign design, decision/optimize/finalize methodology (baseline/experiment/analysis/decision).
- `paper-craft` — oral-writing principles, section-rewrite checklist, the paper-view/evidence-view outline contract (outline/write).
- `review-craft` — review dimensions, evidence-authenticity gate, literature benchmark, review templates (review).
- `rebuttal-craft` — review-matrix→action-plan→evidence-update→response-letter flow + voice rules (rebuttal).
- `intake-rubric` — trust-rank/reconcile pre-existing assets, current-board packet (intake-audit).

**Evidence ladder (shared vocabulary; from `research-method/references/evidence-ladder.md`).** Spend effort in
order, never out of order: `minimum` = the result is executable AND comparable to the baseline; `solid` = the
main comparison is credible — baseline strong + fair, results stable, and **significance testing is present
whenever superiority is claimed**; `maximum` = broaden/polish only AFTER the line is at least `solid`. Keep
`auxiliary/dev` evidence (params, diagnostics, mechanism) distinct from `main/test` (claim-carrying) evidence.

**Comparability contract (shared vocabulary; from `research-method/references/comparability-contract.md`).** A
comparison is trustworthy only when these are explicit: task identity · dataset identity · split contract ·
evaluation script/path · required metric keys · metric directions · source commit/package identity · known
deviations — with a verdict of `usable now | usable with caveats | blocked`. If downstream work would have to
*guess* the comparison contract, the baseline is not ready. Never silently change a dataset/split/metric
definition/eval path; a robustness slice that changes them must be LABELED generalization/stress-test, not
apples-to-apples.

## Methodology-usage audit (Tier-3; required, auditable)

Reading a pack is not optional for stages that have a **required pack**. Required packs by stage:

| stage | required pack(s) | binding typed record + validator (what `applied_as` resolves to) | audited by |
|---|---|---|---|
| intake-audit | `intake-rubric` | trust-ranked intake_asset rows + current-board packet | worker |
| scope, idea | `ideation-rubric` | `idea.select` + `idea validate` (idea selection gate) | worker |
| baseline | `ideation-rubric` + `research-method` | `baseline.contract` + the baseline-contract gate | worker |
| experiment | `research-method` | (no fold-time record) evidence_kind on `claim_evidence`, bound downstream by campaign coverage | worker |
| analysis | `research-method` | `analysis.bridge` + `campaign validate` (campaign coverage + bridge) | worker |
| outline, write | `paper-craft` | `paper_spine` + `outline validate` / `manuscript coverage` (submission_ready) | worker |
| review | `review-craft` | `review.verdict` + `review validate` (review verdict gate) | worker |
| rebuttal | `rebuttal-craft` | response-letter artifact + review-matrix resolution | worker |
| decision, optimize, finalize | `research-method` | `artifact(kind='methodology-usage')` at round close (advisory) | **orchestrator (self-audit)** |

EVERY stage now has a required pack. **Worker stages:** before replying `status=done` you MUST (1) consult the
pack via `$HARNESS knowledge cards`; (2) **produce the stage's typed record and pass its validator** — that
record IS the binding application evidence: `idea.select`+`idea validate`, `baseline.contract`+the baseline
gate, `analysis.bridge`+`campaign validate`, `paper_spine`+`outline validate`/`manuscript coverage`,
`review.verdict`+`review validate` (the `experiment` stage tags `evidence_kind` on `claim_evidence`, bound
downstream by campaign coverage); (3) report `methodology_used[]` `{pack, cards, applied_as=<that record's
id/ref>}`. The orchestrator runs `$HARNESS methodology check` and **rejects any `applied_as` that does not
resolve** to the stage's validated record — methodology usage is no longer free text. Pure background reading
goes in `methodology_consulted[]` (not counted). **Orchestrator-internal stages** (`decision`/`optimize`/
`finalize`) have no typed worker record: the orchestrator records an **`artifact(kind='methodology-usage')`**
at round close (quest-owned, `round_index`, `ref=runs/<q>/methodology/r<r>-<stage>.md`), and `$HARNESS plan
validate` warns at round close if such a closed internal round lacks it (advisory). The typed records remain
**NOT authoritative over DB state** beyond their own validator's flag (the `result`/`claim`/`analysis` rows are
the truth); they are the binding *application evidence* the gates consume.
