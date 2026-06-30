# Research Paradigm Skills

This subtree contains Isomer Labs research-method skills. The skillset is generationed so existing source-derived material remains available while the active v2 core loop can stay concise and semantics-first.

## Generations

| Generation | Path | Role |
| --- | --- | --- |
| v2 | `v2/isomer-rsch-<purpose>-v2/` | Active core research-method skills. These use semantic placeholders such as `[[rsch-object:research-frame]]` and do not bind outputs to storage yet. |
| v1 | `v1/isomer-rsch-<purpose>-v1/` | Preserved first-generation Isomer adaptations of source skills. These keep the richer storage, lifecycle, policy, and paper-facing guidance for reference and compatibility. |

The root directory should not contain active flat `isomer-rsch-*` skill folders. New core research work should target v2 unless a preserved paper-facing or intake behavior is explicitly needed from v1.

## V2 Core Skills

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-shared-v2` | Shared v2 loop and semantic placeholder contract. |
| `isomer-rsch-scout-v2` | Clarify the research frame, metric direction, comparator neighborhood, and next route. |
| `isomer-rsch-baseline-v2` | Establish the comparator and metric basis, or state a waiver or blocker. |
| `isomer-rsch-idea-v2` | Select one falsifiable hypothesis from the current frame and comparator. |
| `isomer-rsch-optimize-v2` | Manage algorithm-first candidate frontiers and promote one route. |
| `isomer-rsch-experiment-v2` | Test one selected hypothesis and interpret the result. |
| `isomer-rsch-analysis-v2` | Run focused follow-up analysis for a result. |
| `isomer-rsch-decision-v2` | Make one evidence-backed route choice. |
| `isomer-rsch-finalize-v2` | Summarize final claims, limits, and next action. |
| `isomer-rsch-science-v2` | Check scientific computation, data, package, simulation, or model validity. |

The v2 loop is `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`. `isomer-rsch-optimize-v2` overlays hypothesis, experiment, and analysis when candidate search is the work. `isomer-rsch-science-v2` supports any stage whose trust depends on scientific computation or data validity.

## V2 Placeholder Contract

V2 skills name reusable research objects with `[[rsch-object:<id>]]` placeholders. The authoritative registry is `v2/isomer-rsch-shared-v2/references/semantic-placeholders.md`.

These placeholders define semantics only. They are not yet bound to Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, storage label, or database schema. Storage binding belongs to a later design pass after the placeholder meanings are stable.

## V1 Preserved Skills

The v1 generation contains all previous `isomer-rsch-*` skills with `-v1` suffixes, including intake, write, review, rebuttal, paper-outline, paper-plot, and figure-polish. Use v1 when a team or task still needs the richer first-generation guidance, especially paper-facing workflows not yet rewritten for v2.

## Skill Writing Constraints

V2 `SKILL.md` files should use valid frontmatter with `name` and `description`, a near-top `## Workflow`, numbered workflow steps, semantic inputs, semantic outputs, guardrails, and explicit reference routing when references exist. The `agents/openai.yaml` manifest must use the same generation-suffixed skill name in `interface.display_name` and `interface.default_prompt`.

Do not add active storage, runtime, scheduler, provider, lifecycle, or concrete path binding to v2 skill guidance. If a v2 skill needs to name a research object, add or reuse a registered `[[rsch-object:<id>]]` placeholder instead.

Operator/admin skills belong under `skillset/operator/` with `isomer-admin-*` names. Service skills belong under `skillset/service/` with `isomer-srv-*` names.
