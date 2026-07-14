# Kaoju Survey Process Use Cases

Status: Proposed

## Purpose

Capture refined, user-facing use cases for the Kaoju evidence-led survey workflow: how a user (or Topic Actor) starts from a topic, proposes a survey direction, collects online information, analyzes it, tests claims with code when appropriate, and writes structured survey records and papers.

## Artifacts

- [Feature Requirement](feature-requirement.md)
- [Use Cases](usecases/README.md)
- [Design](design/README.md)
- [Agent Task](agent-task.md)
- [ADRs](adrs/)

## Current Stage

Feature requirement and use cases `uc-01` through `uc-10` are designed. The OpenSpec change `revise-kaoju-survey-process` defines the proposed system-skill and `isomer-cli` refactor, specifications, and implementation tasks.

## Related Context

- Kaoju skill suite: `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`
- Existing analysis of the Kaoju suite: `.imsight-arts/agent-skill-handling/analysis/kaoju-suite/`
- Current topic workspace example: `isomer-content/topic-ws/predictive-memory-tiering-survey/`

## Decisions

- The use cases serve human researchers and the Topic Actors conducting their human-orchestrated work. Topic Actor remains the canonical worker identity rather than a synonym for the human.
- Agent skills own research judgment and user-intent procedures; typed `isomer-cli` services own deterministic persistence, path resolution, acquisition, dispatch, conversion, build, deployment, and launch operations.
- UC-01 through UC-10 cover the requested survey-to-paper, wiki, source-ingestion, environment-preparation, and trial lifecycle. Additional behavior belongs in refinements unless it introduces a distinct actor goal.
