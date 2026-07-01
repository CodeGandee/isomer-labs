# Research Paradigm Skills

This subtree contains Isomer Labs research-method skills. The skillset is generationed so existing source-derived material remains available while the active v2 research and companion-skill surface can stay concise and semantics-first.

## Generations

| Generation | Path | Role |
| --- | --- | --- |
| v2 | `v2/isomer-rsch-<purpose>-v2/` | Active current research-method and companion skills. Core loop skills use semantic placeholders such as `[[rsch-object:research-frame]]`; refactor-migrated companion skills use local placeholders such as `<PAPER_CONTRACT>`. V2 keeps skill outputs semantic; `isomer-rsch-workspace-mgr-v2` performs the topic-specific bootstrap pass that maps placeholders to available, planned, custom-needed, blocked, or deferred storage surfaces. |
| v1 | `v1/isomer-rsch-<purpose>-v1/` | Preserved first-generation Isomer adaptations of source skills. These keep the richer storage, lifecycle, policy, and paper-facing guidance for reference and compatibility. |

The root directory should not contain active flat `isomer-rsch-*` skill folders. New research work should target v2 unless a preserved intake behavior or older compatibility surface is explicitly needed from v1.

## V2 Core Research Skills

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

## V2 Workspace Bootstrap Skill

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-workspace-mgr-v2` | Prepare the post-specialization research bootstrap contract for v2 skills, including workspace context, semantic label planning, placeholder binding, Agent Workspace access posture, validation, and blockers. |

Run this skill after Topic Team Specialization and standard Topic Workspace initialization, before ordinary v2 research skills start writing durable placeholder bodies. The Topic Service Master may perform this pass from the Topic Workspace cwd; when that optional agent is not running, the Project Operator Session or Operator Agent performs the same bounded work.

## V2 Paper Writing Skills

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-write-v2` | Draft or revise paper, report, summary, and manuscript text from bounded evidence. |
| `isomer-rsch-paper-outline-v2` | Build or repair a paper-native outline, claim boundary, method abstraction, and writing plan. |
| `isomer-rsch-paper-plot-v2` | Adapt bundled plotting templates into first-pass publication figures. |
| `isomer-rsch-figure-polish-v2` | Render, inspect, revise, export, and record durable academic figures. |
| `isomer-rsch-review-v2` | Audit a substantial draft or paper-like report and route concrete fixes. |
| `isomer-rsch-rebuttal-v2` | Normalize reviewer feedback, route required fixes, and assemble a response package. |
| `isomer-rsch-nature-data-v2` | Prepare Nature-style Data Availability statements, repository plans, dataset citations, and FAIR metadata checks. |
| `isomer-rsch-nature-figure-v2` | Create, revise, audit, or polish Nature-grade figures with one selected Python or R backend. |
| `isomer-rsch-nature-paper2ppt-v2` | Build a complete Chinese PPTX presentation from a scientific paper or paper-derived notes. |
| `isomer-rsch-nature-polishing-v2` | Polish, restructure, or translate academic prose into Nature-leaning English without hiding evidence gaps. |

These paper-writing skills were refactor-migrated from the paper-writing source analysis index. Each target directory keeps source provenance under `org/`, a local migration plan under `migrate/`, copied runtime support files, and an `agents/openai.yaml` manifest.

## V2 Runtime and Traceability Layout

Active v2 execution guidance lives in each skill's `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`. Migration and traceability material lives under `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, provenance files, license notices, and deferred-resource notes. Those files preserve review history and source context; they are not required runtime inputs when invoking an installed skill.

## V2 Placeholder Contract

V2 core-loop skills name reusable research objects with `[[rsch-object:<id>]]` placeholders. The authoritative registry is `v2/isomer-rsch-shared-v2/references/semantic-placeholders.md`.

Refactor-migrated companion skills may name handoff objects with uppercase angle-bracket placeholders such as `<PAPER_CONTRACT>`. Those placeholders are local to the skill and must be listed in that skill's `migrate/placeholders.md`.

These placeholders define semantics only. They are not yet bound to Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, storage label, or database schema. Storage binding belongs to a later design pass after the placeholder meanings are stable.

## V1 Preserved Skills

The v1 generation contains all previous `isomer-rsch-*` skills with `-v1` suffixes, including intake, write, review, rebuttal, paper-outline, paper-plot, and figure-polish. Use v1 when a team or task still needs the richer first-generation guidance or compatibility with older paper-facing references.

## Skill Writing Constraints

V2 `SKILL.md` files should use valid frontmatter with `name` and `description`, a near-top `## Workflow`, numbered workflow steps, semantic inputs, semantic outputs, guardrails, and explicit reference routing when references exist. The `agents/openai.yaml` manifest must use the same generation-suffixed skill name in `interface.display_name` and `interface.default_prompt`.

Do not add active storage, runtime, scheduler, provider, lifecycle, or concrete path binding to v2 skill guidance. If a v2 skill needs to name a research object, add or reuse a registered `[[rsch-object:<id>]]` placeholder instead.

Operator/admin skills belong under `skillset/operator/` with `isomer-admin-*` names. Service skills belong under `skillset/service/` with `isomer-srv-*` names.
