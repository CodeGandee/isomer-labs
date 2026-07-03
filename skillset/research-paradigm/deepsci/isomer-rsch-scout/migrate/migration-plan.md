# Scout Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/scout`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-scout`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-scout.md`.
- Exclusions from deep inspection: none. The source skill contains only an entrypoint and five directly linked reference pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the sentence. Runtime pages use the narrowest term that matches the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Findings, Evidence Items, Decision Records, and user-provided Research Topic context. |
| scout stage | `isomer-rsch-scout` as a bounded research-framing skill. |
| baseline next anchor | `isomer-rsch-baseline`, or a baseline route recorded through `<NEXT_ROUTE_DECISION>`. |
| idea next anchor | `isomer-rsch-idea`, or an idea route recorded through `<NEXT_ROUTE_DECISION>`. |
| remain in scout | A blocked or continued scout route recorded through `<SCOUT_BLOCKER_RECORD>` or `<NEXT_ROUTE_DECISION>`. |
| memory cards | Workspace Runtime-backed compatibility memory results, summarized as `<SCOUT_MEMORY_REUSE_NOTE>` and `<SCOUT_CONTINUITY_UPDATE>`. |
| paper/repo/benchmark neighborhood | Literature Provider Binding results, official repositories, benchmark documentation, and source Artifacts summarized through `<LITERATURE_SCOUTING_REPORT>` or `<SCOUT_DISCOVERY_LEDGER>`. |
| evaluation contract | `<EVALUATION_CONTRACT>`. |
| baseline shortlist | `<BASELINE_SHORTLIST>`. |
| literature scouting report | `<LITERATURE_SCOUTING_REPORT>`. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.list_recent(...)` | Use the Isomer DeepScientist-compatible extension harness when compatibility is required: `isomer-cli ext deepsci call memory.list_recent --input-json <json-object>`. Summarize the result as `<SCOUT_MEMORY_REUSE_NOTE>`. |
| `memory.search(...)` | Use `isomer-cli ext deepsci call memory.search --input-json <json-object>` when compatibility is required. Summarize the result as `<SCOUT_MEMORY_REUSE_NOTE>`. |
| `memory.write(...)` | Use `isomer-cli ext deepsci call memory.write --input-json <json-object>` when a reusable scout conclusion must be preserved before storage binding is finalized. Summarize the write as `<SCOUT_CONTINUITY_UPDATE>`. |
| `artifact.read_quest_documents(...)` and `artifact.get_quest_state(...)` | Use Isomer Workspace Runtime and Artifact lookup when available; use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` only for compatibility. Summarize consumed context as `<SCOUT_CONTEXT_BRIEF>`. |
| `artifact.git(...)` | Prefer Isomer repository and Artifact inspection surfaces. When a compatibility call is needed, use `isomer-cli ext deepsci call artifact.git --input-json <json-object>`. Fold relevant evidence into `<SCOUT_DISCOVERY_LEDGER>`. |
| `artifact.arxiv(paper_id=..., full_text=False)` | Prefer a Literature Provider Binding or Isomer paper-reading extension. When a compatibility call is needed, use `isomer-cli ext deepsci call artifact.arxiv --input-json <json-object>`. Fold retained paper evidence into `<LITERATURE_SCOUTING_REPORT>`. |
| `bash_exec(...)` only for shell, CLI, Python, git, npm, uv, or repo inspection | Runtime pages describe this as an Execution Adapter Command Request or DeepScientist-compatible `bash_exec` extension call when command execution is necessary. The scout skill should prefer Workspace Runtime, Artifact, literature, and repository inspection surfaces before shell execution. |
| DeepXiv when declared available | Treat as a provider-bound paper discovery route through Literature Provider Binding or Research Operation Extension Point, not as core Isomer terminology. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use placeholders defined in `migrate/placeholders.md`:

- `<SCOUT_CONTEXT_BRIEF>`
- `<SCOUT_MEMORY_REUSE_NOTE>`
- `<SCOUT_MINIMUM_UNKNOWNS>`
- `<SCOUT_DISCOVERY_LEDGER>`
- `<LITERATURE_SCOUTING_REPORT>`
- `<EVALUATION_CONTRACT>`
- `<BASELINE_SHORTLIST>`
- `<NEXT_ROUTE_DECISION>`
- `<SCOUT_BLOCKER_RECORD>`
- `<SCOUT_CONTINUITY_UPDATE>`

These placeholders cover source mentions of `brief.md`, `plan.md`, `status.md`, `SUMMARY.md`, baseline artifacts, recent paper or knowledge memory cards, search ledgers, reference buckets, evaluation contracts, baseline shortlists, next anchors, blocked scout results, and memory writes.

## Unmatched Skill-Route Substitutions

- Source `baseline` maps to `isomer-rsch-baseline`.
- Source `idea` maps to `isomer-rsch-idea`.
- Source continued `scout` maps to `isomer-rsch-scout` with `<SCOUT_BLOCKER_RECORD>` or `<NEXT_ROUTE_DECISION>`.
- DeepXiv is treated as a provider-bound literature route rather than a missing skill.
- No source skill route currently requires a `missing-isomer-skill` placeholder.

## Environment Substitutions

- The source skill does not require `venv`, but it prohibits native shell execution and routes commands through `bash_exec(...)`.
- Runtime Isomer pages prefer Workspace Runtime, Artifact, Literature Provider Binding, repository inspection, and Execution Adapter Command Request surfaces.
- When command execution is unavoidable, the migrated skill should use Isomer CLI or adapter surfaces from the active Pixi-managed Project or Topic Workspace context rather than inventing a separate environment.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders includes a sentence pointing to that registry.

## Rewrite Targets

- `SKILL.md`: refactor the source control surface into native Isomer research language.
- `references/operational-guidance.md`: rewrite the tactical scout workflow using Research Topic, Topic Workspace, Workspace Runtime, Artifact, Evidence Item, Gate, Decision Record, and provider-bound discovery language.
- `references/paper-triage-playbook.md`: rewrite bounded paper, repository, and benchmark triage guidance.
- `references/literature-scout-template.md`: rewrite the durable literature report template with placeholders and Isomer provenance language.
- `references/eval-contract-template.md`: preserve and refactor the source evaluation contract template.
- `references/evaluation-contract-template.md`: compatibility redirect for the earlier production DeepSci expanded filename.
- `references/baseline-shortlist-template.md`: rewrite the baseline shortlist template around comparator route decisions.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Check entry fit | `SKILL.md` Match signals, Do not use when, Preconditions and gate, Exit criteria; `references/operational-guidance.md` planning and stop notes. | `references/operational-guidance.md` |
| Reconstruct the current frame | `SKILL.md` Control workflow step 1, Truth sources, Preconditions and gate; `references/operational-guidance.md` detailed workflow step 1. | `references/operational-guidance.md` |
| Reuse prior knowledge first | `SKILL.md` Constraints, Tool discipline, Truth sources; `references/operational-guidance.md` memory note; `references/paper-triage-playbook.md` search order and reuse discipline. | `references/operational-guidance.md`, `references/paper-triage-playbook.md` |
| Name the minimum unknowns | `SKILL.md` Control workflow step 2, One-sentence summary, AVOID/pitfalls; `references/operational-guidance.md` minimum unknowns and unknown classification. | `references/operational-guidance.md` |
| Search the unresolved neighborhood | `SKILL.md` Control workflow step 3, Constraints, Tool discipline, Non-negotiable rules; `references/paper-triage-playbook.md`; `references/literature-scout-template.md`. | `references/paper-triage-playbook.md`, `references/literature-scout-template.md` |
| Clarify route-facing outputs | `SKILL.md` Control workflow step 4, Validation; `references/eval-contract-template.md`; `references/baseline-shortlist-template.md`; `references/literature-scout-template.md`. | `references/eval-contract-template.md`, `references/baseline-shortlist-template.md`, `references/literature-scout-template.md` |
| Record the next route or blocker | `SKILL.md` Control workflow step 5, Blocked-state handling, Exit criteria; `references/operational-guidance.md`. | `references/operational-guidance.md` |
| Preserve continuity | `SKILL.md` Interaction discipline, Operational guidance, Exit criteria; `references/operational-guidance.md`; `references/literature-scout-template.md`. | `references/operational-guidance.md`, `references/literature-scout-template.md` |

The existing `agents/openai.yaml` already uses the correct production DeepSci skill name and remains unchanged.

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Enter only when framing ambiguity blocks baseline, idea, or route selection.
- Exit quickly when the frame is already stable.
- Reconstruct the current frame before broad search.
- Reuse memory and durable context before new discovery.
- Identify only unknowns that change the next route.
- Search actively when local evidence is insufficient, but stop on route clarity.
- Prefer paper discovery and official sources for paper-centric work, then read papers through the appropriate provider only when needed.
- Make task, dataset, split, metric, fairness, and useful-improvement rules explicit.
- Produce a small baseline shortlist with attach, import, reproduce, or reject recommendations.
- Search for disconfirming evidence, not only supporting evidence.
- Record a literature scouting report when external search materially changes the route.
- Preserve blocked states with missing input, impact, blocked route, and concrete user or source need.
- Route to baseline by default unless a trustworthy comparator is already durable enough for idea work.
