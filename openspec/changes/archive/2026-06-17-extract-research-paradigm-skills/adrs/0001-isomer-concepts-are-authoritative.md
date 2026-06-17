# Isomer Concepts Are Authoritative

## Status

accepted

## Context

The migration source is DeepScientist, which provides useful research-stage behavior through skills such as scout, baseline, idea, experiment, analysis, decision, finalize, write, review, rebuttal, and science. DeepScientist also brings its own runtime model: quests, quest roots, quest-local skill projection, `.ds` state, `artifact.*`, `memory.*`, `bash_exec(...)`, and DeepXiv.

Isomer Labs already has domain language for Project, Project Manifest, Isomer Workspace, Workspace Runtime, Research Thread, Research Task, Run, Research Branch, Operator Agent, Agent Role, Agent Instance, Capability Binding, Coordination Policy, Execution Adapter, Artifact, Evidence Item, Finding, Decision Record, Gate, and Provenance Record.

The user clarified that Isomer Labs must remain authoritative. We will not introduce new Isomer concepts just because DeepScientist needs them. Missing equivalents must be reviewed later and either mapped to existing Isomer concepts or accepted through a separate Isomer design decision.

## Decision

The migrated research-paradigm skills will use Isomer Labs domain language as the canonical vocabulary. DeepScientist names may appear only in provenance notes, source-analysis references, or explicit mapping guidance.

DeepScientist-specific concepts do not create Isomer concepts by default. When a DeepScientist behavior has no settled Isomer framing, the skill extraction must classify it as one of:

- Existing Isomer concept: use the canonical Isomer term.
- Source implementation detail: omit it or mention it only as provenance.
- Unsettled concrete surface: mark it as `yet-to-be-determined`.
- Candidate platform gap: record it for review, but do not treat it as a settled concept inside the skills.

## Considered Options

- Use Isomer concepts as authoritative and map DeepScientist behavior into them.
- Add DeepScientist concepts as Isomer synonyms to reduce migration effort.
- Create a DeepScientist-compatible compatibility layer before skill extraction.

## Consequences

- The skills can preserve DeepScientist methodology without inheriting DeepScientist's workspace model.
- Terms such as `quest`, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, quest branch, and quest worktree must not be required runtime operations in the new skills.
- Gaps become visible review items instead of hidden provisional platform design.
- Future introduction of a new Isomer concept requires a separate accepted ADR or spec update.
