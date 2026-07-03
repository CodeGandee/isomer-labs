# Research Paradigm Skills

This subtree contains the production DeepSci research-method skills for Isomer Labs. The active skill root is `deepsci/`; retired `v1` and temporary `v2` skill roots are intentionally absent.

## Production DeepSci Layout

| Path | Role |
| --- | --- |
| `deepsci/isomer-rsch-<purpose>/` | Active production research-method and companion skills. Core loop skills use semantic placeholders such as `[[rsch-object:research-frame]]`; refactor-migrated companion skills use local placeholders such as `<PAPER_CONTRACT>`. |
| Analysis notes | Design notes used while adapting upstream research-method skills. This is not an active runtime input for installed skills. |
| `licenses/` | Shared license material for adapted upstream content. |

The root directory does not contain active flat `isomer-rsch-*` skill folders. New research work should target `deepsci/` and suffixless skill names such as `isomer-rsch-scout`.

## Core Research Skills

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-shared` | Shared production loop and semantic placeholder contract. |
| `isomer-rsch-scout` | Clarify the research frame, metric direction, comparator neighborhood, and next route. |
| `isomer-rsch-baseline` | Establish the comparator and metric basis, or state a waiver or blocker. |
| `isomer-rsch-idea` | Select one falsifiable hypothesis from the current frame and comparator. |
| `isomer-rsch-optimize` | Manage algorithm-first candidate frontiers and promote one route. |
| `isomer-rsch-experiment` | Test one selected hypothesis and interpret the result. |
| `isomer-rsch-analysis` | Run focused follow-up analysis for a result. |
| `isomer-rsch-decision` | Make one evidence-backed route choice. |
| `isomer-rsch-finalize` | Summarize final claims, limits, and next action. |
| `isomer-rsch-science` | Check scientific computation, data, package, simulation, or model validity. |

The production loop is `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`. `isomer-rsch-optimize` overlays hypothesis, experiment, and analysis when candidate search is the work. `isomer-rsch-science` supports any stage whose trust depends on scientific computation or data validity.

## Workspace Bootstrap Skill

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-workspace-mgr` | Prepare the post-specialization research bootstrap contract, including workspace context, semantic label planning, placeholder binding, Agent Workspace access posture, validation, and blockers. |

Run this skill after Topic Team Specialization and standard Topic Workspace initialization, before ordinary production research skills start writing durable placeholder bodies. The Topic Service Master may perform this pass from the Topic Workspace cwd; when that optional agent is not running, the Project Operator Session or Operator Agent performs the same bounded work.

## Paper Writing Skills

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-write` | Draft or revise paper, report, summary, and manuscript text from bounded evidence. |
| `isomer-rsch-paper-outline` | Build or repair a paper-native outline, claim boundary, method abstraction, and writing plan. |
| `isomer-rsch-paper-plot` | Adapt bundled plotting templates into first-pass publication figures. |
| `isomer-rsch-figure-polish` | Render, inspect, revise, export, and record durable academic figures. |
| `isomer-rsch-review` | Audit a substantial draft or paper-like report and route concrete fixes. |
| `isomer-rsch-rebuttal` | Normalize reviewer feedback, route required fixes, and assemble a response package. |
| `isomer-rsch-nature-data` | Prepare Nature-style Data Availability statements, repository plans, dataset citations, and FAIR metadata checks. |
| `isomer-rsch-nature-figure` | Create, revise, audit, or polish Nature-grade figures with one selected Python or R backend. |
| `isomer-rsch-nature-paper2ppt` | Build a complete Chinese PPTX presentation from a scientific paper or paper-derived notes. |
| `isomer-rsch-nature-polishing` | Polish, restructure, or translate academic prose into Nature-leaning English without hiding evidence gaps. |

These paper-writing skills were refactor-migrated from the paper-writing source analysis index. Each target directory may keep source provenance under `org/`, a local migration plan under `migrate/`, copied runtime support files, and an `agents/openai.yaml` manifest.

## Runtime and Traceability Layout

Active execution guidance lives in each skill's `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`. Migration and traceability material lives under `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, provenance files, license notices, and deferred-resource notes. Those files preserve review history and source context; they are not required runtime inputs when invoking an installed skill.

## Placeholder Contract

Core-loop skills name reusable research objects with `[[rsch-object:<id>]]` placeholders. The authoritative registry is `deepsci/isomer-rsch-shared/references/semantic-placeholders.md`.

Refactor-migrated companion skills may name handoff objects with uppercase angle-bracket placeholders such as `<PAPER_CONTRACT>`. Those placeholders are local to the skill and must be listed in that skill's `migrate/placeholders.md`.

These placeholders define semantics only. Storage binding belongs in local `placeholder-bindings.md` pages and the workspace manager bootstrap pass, not in freeform method prose.

## Retired Generations

The retired `v1` skills and temporary `v2` paths are no longer active and are not kept as compatibility aliases. Use git history for historical reference.

## Skill Writing Constraints

Production `SKILL.md` files should use valid frontmatter with `name` and `description`, a near-top `## Workflow`, numbered workflow steps, semantic inputs, semantic outputs, guardrails, and explicit reference routing when references exist. The `agents/openai.yaml` manifest must use the same suffixless skill name in `interface.display_name` and `interface.default_prompt`.

Do not add unbounded active storage, runtime, scheduler, provider, lifecycle, or concrete path binding to method guidance. If a core skill needs to name a research object, add or reuse a registered `[[rsch-object:<id>]]` placeholder instead.

Operator/admin skills belong under `skillset/operator/` with `isomer-admin-*` names. Service skills belong under `skillset/service/` with `isomer-srv-*` names.
