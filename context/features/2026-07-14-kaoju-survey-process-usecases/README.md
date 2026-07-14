# Kaoju Survey Process Use Cases

Status: Draft

## Purpose

Capture refined, user-facing use cases for the Kaoju evidence-led survey workflow: how a user (or Topic Actor) starts from a topic, proposes a survey direction, collects online information, analyzes it, tests claims with code when appropriate, and writes structured survey records and papers.

## Artifacts

- [Feature Requirement](feature-requirement.md)
- [Use Cases](usecases/README.md)
- [Design](design/README.md)
- [Agent Task](agent-task.md)
- [ADRs](adrs/)

## Current Stage

Feature requirement drafted; use cases `uc-01` (survey direction), `uc-02` (online collection and reading list), and `uc-03` (ingest reading item in depth) are designed. Remaining use cases will cover code testing, synthesis, and paper writing.

## Related Context

- Kaoju skill suite: `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`
- Existing analysis of the Kaoju suite: `.imsight-arts/agent-skill-handling/analysis/kaoju-suite/`
- Current topic workspace example: `isomer-content/topic-ws/predictive-memory-tiering-survey/`

## Open Questions

- Should these use cases target human researchers, Topic Actors, or both?
- Should the workflow be exposed as CLI commands, agent-skill invocations, or both?
- How many use cases are needed to cover the full survey-to-paper lifecycle?
