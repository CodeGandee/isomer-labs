---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Kaoju Research Idea Mapping

Use the independently installed `isomer-op-entrypoint->research-ideas` skill as the authoritative portfolio contract. This page maps Kaoju profiles to that contract and does not depend on DeepSci.

## Direction Set v2

`KAOJU:DIRECTION-SET` remains the Kaoju Decision Record. The Direction Set as a whole is not a Research Idea. Each actor-confirmed durable proposal object realizes one canonical Research Idea through its exact path `$.sections.proposals[<index>]`.

For every proposal, author:

- a stable semantic `idea_id`, with the source-local direction `id` retained as an alias;
- non-empty `title`, `summary`, research question, boundary, source classes, coverage date, expected depth, deliverables, and empirical feasibility;
- the exact `source_json_path` and one shared proposal `generation_id`;
- an authored decision outcome and disposition rationale;
- a closure reason when the outcome is `closed`;
- whether the current acceptance changes disposition and therefore requires a transition.

Put `research_idea_effects` in the v2 payload with `atomic=true` and `artifact_family=kaoju`. List every proposal idea with explicit canonical facets and exact source path. Add one generation group with exact membership, one Decision Record option for every proposal, and each justified transition with actor, rationale, and durable refs. Selected proposals transition to `selected`. A merely unselected proposal remains `open`; it is not rejected, deferred, or closed unless the actor says so.

Actor-confirmed acceptance must use the active v2 binding returned by `ext kaoju bindings describe KAOJU:DIRECTION-SET`. The record response must contain every promised canonical ref. Query the resulting ideas and Direction Set decision context, resolve each realization object, and run canonical idea validation before checkpointing `choose-directions` complete.

## Revisions and Concept Changes

When an accepted Direction Set revision changes wording, boundary detail, evidence depth, or deliverables without changing a proposal concept, retain the `idea_id`, add a realization to the new exact proposal object, and omit a state transition when the state did not change. When a proposal becomes a distinct concept, create a new `idea_id` and an explicit justified concept-lineage edge. Record-level `revision_of` remains separate.

Legacy Direction Set v1 remains readable. Preview migration before apply, preserve direction ids as aliases, record only directly justified option outcomes, leave unsupported facets `unknown`, and never invent rationale, closure reasons, or lineage.

## Downstream Kaoju Effects

- `isomer-kaoju-frame` owns proposal creation and actor-confirmed Direction Set decisions.
- `isomer-kaoju-discover` keeps papers, repositories, datasets, search routes, and reading-list candidates as Source Identities or survey material. Starting an explicitly accepted direction task may transition its existing idea to `exploring` with the Research Task ref.
- `isomer-kaoju-trial` may update exploration or evidence only from an accepted terminal trial Artifact, Evidence Item, Finding, Research Task, or Run.
- `isomer-kaoju-compare` may assess an existing direction from an accepted comparison result. Works and method candidates are not ideas unless an actor promotes a distinct conceptual direction.
- `isomer-kaoju-audit` may record an evidence assessment when the accepted audit directly evaluates the direction. Findings and repair routes remain Findings or Research Tasks.
- `isomer-kaoju-synthesize` may mark focused direction exploration complete and update evidence when accepted synthesis refs justify it. Claims remain Research Claims.
- `isomer-kaoju-write` may add a realization when a paper-facing object restates the same direction. Paper sections, structure choices, figures, and manuscripts remain Artifacts.

Every downstream state change uses an explicit canonical transition with expected current state, actor, rationale, and terminal refs. Evidence does not change decision state, and survey progress does not create new concepts automatically.
