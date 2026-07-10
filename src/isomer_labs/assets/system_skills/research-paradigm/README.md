# Research Paradigm Skills

This subtree contains two optional production research-paradigm families for Isomer Labs. `deepsci/` supports hypothesis-driven new-method research; `kaoju/` supports evidence-led surveys of literature, codebases, datasets, and models, including governed first-hand trials when a survey question requires them. Retired `v1` and temporary `v2` skill roots are intentionally absent.

## Production Families

| Path | Role |
| --- | --- |
| `deepsci/isomer-deepsci-<purpose>/` | Hypothesis-driven research stages, experiments, analysis, decisions, writing, and publication support. |
| `kaoju/isomer-kaoju-<purpose>/` | Literature-first survey framing, discovery, material acquisition, source examination, reproduction, comparison, audit, and synthesis. |

Kaoju maps and verifies existing work. DeepSci develops or evaluates a research route around a hypothesis and comparator. A task may hand evidence between families, but each family retains its own procedure and evidence contract.

## Production DeepSci Layout

| Path | Role |
| --- | --- |
| `deepsci/isomer-deepsci-<purpose>/` | Active production research-method and companion skills. Core loop skills use semantic placeholders such as `[[rsch-object:research-frame]]`; refactor-migrated companion skills use local placeholders such as `<PAPER_CONTRACT>`. |
| Analysis notes | Design notes used while adapting upstream research-method skills. This is not an active runtime input for installed skills. |
| `licenses/` | Shared license material for adapted upstream content. |

The root directory does not contain active flat `isomer-deepsci-*` skill folders. New research work should target `deepsci/` and suffixless skill names such as `isomer-deepsci-scout`.

DeepSci and Kaoju are domain extension families, not a generic extension bucket. Domain extensions use the `isomer-<extension-name>-<purpose>` convention described in the packaged system-skill README: `isomer-deepsci-<purpose>` and `isomer-kaoju-<purpose>`. Cross-domain helper interfaces remain under `isomer-misc-*`.

## Production Kaoju Layout

The Kaoju family contains one pipeline, shared and workspace contracts, and focused frame, discover, acquire, examine, reproduce, compare, audit, and synthesize skills. Its pipeline exposes seven bounded survey procedures, grouped `manage-survey` and `manage-dataset` helpers, and `help`. Generic repository maintenance, environment repair, and resume behavior remain context inside a selected survey procedure.

Active Kaoju guidance lives in `SKILL.md`, `agents/openai.yaml`, and directly linked local `commands/` or `references/`. It uses existing Topic Workspace, provider, environment, execution, Gate, and research-recording owners rather than defining a Kaoju runtime database or provider.

## Core Research Skills

| Skill | Purpose |
| --- | --- |
| `isomer-deepsci-shared` | Shared production loop and semantic placeholder contract. |
| `isomer-deepsci-scout` | Clarify the research frame, metric direction, comparator neighborhood, and next route. |
| `isomer-deepsci-baseline` | Establish the comparator and metric basis, or state a waiver or blocker. |
| `isomer-deepsci-idea` | Select one falsifiable hypothesis from the current frame and comparator. |
| `isomer-deepsci-optimize` | Manage algorithm-first candidate frontiers and promote one route. |
| `isomer-deepsci-experiment` | Test one selected hypothesis and interpret the result. |
| `isomer-deepsci-analysis` | Run focused follow-up analysis for a result. |
| `isomer-deepsci-decision` | Make one evidence-backed route choice. |
| `isomer-deepsci-finalize` | Summarize final claims, limits, and next action. |
| `isomer-deepsci-science` | Check scientific computation, data, package, simulation, or model validity. |

The production loop is `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`. `isomer-deepsci-optimize` overlays hypothesis, experiment, and analysis when candidate search is the work. `isomer-deepsci-science` supports any stage whose trust depends on scientific computation or data validity.

## Workspace Bootstrap Skill

| Skill | Purpose |
| --- | --- |
| `isomer-deepsci-workspace-mgr` | Prepare the post-specialization research bootstrap contract, including workspace context, semantic label planning, placeholder binding, Agent Workspace access posture, validation, and blockers. |

Run this skill after Topic Team Specialization and standard Topic Workspace initialization, before ordinary production research skills start writing durable placeholder bodies. The Topic Service Master may perform this pass from the Topic Workspace cwd; when that optional agent is not running, the Project Operator Session or Operator Agent performs the same bounded work.

## Paper Writing Skills

| Skill | Purpose |
| --- | --- |
| `isomer-deepsci-write` | Draft or revise paper, report, summary, and manuscript text from bounded evidence. |
| `isomer-deepsci-paper-outline` | Build or repair a paper-native outline, claim boundary, method abstraction, and writing plan. |
| `isomer-deepsci-paper-plot` | Adapt bundled plotting templates into first-pass publication figures. |
| `isomer-deepsci-figure-polish` | Render, inspect, revise, export, and record durable academic figures. |
| `isomer-deepsci-review` | Audit a substantial draft or paper-like report and route concrete fixes. |
| `isomer-deepsci-rebuttal` | Normalize reviewer feedback, route required fixes, and assemble a response package. |
| `isomer-deepsci-nature-data` | Prepare Nature-style Data Availability statements, repository plans, dataset citations, and FAIR metadata checks. |
| `isomer-deepsci-nature-figure` | Create, revise, audit, or polish Nature-grade figures with one selected Python or R backend. |
| `isomer-deepsci-nature-paper2ppt` | Build a complete Chinese PPTX presentation from a scientific paper or paper-derived notes. |
| `isomer-deepsci-nature-polishing` | Polish, restructure, or translate academic prose into Nature-leaning English without hiding evidence gaps. |

These paper-writing skills were refactor-migrated from the paper-writing source analysis index. Each target directory may keep source provenance under `org/`, a local migration plan under `migrate/`, copied runtime support files, and an `agents/openai.yaml` manifest.

## Runtime and Traceability Layout

Active execution guidance lives in each skill's `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`. Migration and traceability material lives under `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, provenance files, license notices, and deferred-resource notes. Those files preserve review history and source context; they are not required runtime inputs when invoking an installed skill.

## Placeholder Contract

Core-loop skills name reusable research objects with `[[rsch-object:<id>]]` placeholders. The authoritative registry is `deepsci/isomer-deepsci-shared/references/semantic-placeholders.md`.

Refactor-migrated companion skills may name handoff objects with uppercase angle-bracket placeholders such as `<PAPER_CONTRACT>`. Those placeholders are local to the skill and must be listed in that skill's `migrate/placeholders.md`.

These placeholders define semantics only. Storage binding belongs in local `placeholder-bindings.md` pages and the workspace manager bootstrap pass, not in freeform method prose.

## Retired Generations

The retired `v1` skills and temporary `v2` paths are no longer active and are not kept as compatibility aliases. Use git history for historical reference.

## Skill Writing Constraints

Production `SKILL.md` files should use valid frontmatter with `name` and `description`, a near-top `## Workflow`, numbered workflow steps, semantic inputs, semantic outputs, guardrails, and explicit reference routing when references exist. The `agents/openai.yaml` manifest must use the same suffixless skill name in `interface.display_name` and `interface.default_prompt`.

Do not add unbounded active storage, runtime, scheduler, provider, lifecycle, or concrete path binding to method guidance. If a core skill needs to name a research object, add or reuse a registered `[[rsch-object:<id>]]` placeholder instead.

Operator skills belong under `skillset/operator/` with `isomer-op-*` names. Service skills belong under `skillset/service/` with `isomer-srv-*` names.
