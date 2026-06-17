## 1. Source Inventory and Setup

- [x] 1.1 Review `context/explore/deepscientist-skill-analysis/README.md` and confirm the core source skills for the first pass.
- [x] 1.2 Review `teams/deepsci-org/source/team-design.md` and identify DeepScientist-specific role names and source references to replace.
- [x] 1.3 Create `skillset/research-paradigm/` with source provenance and license notice files for DeepScientist-derived material.
- [x] 1.4 Create empty core skill folders using the `isomer-labs-research-<purpose>` naming convention.

## 2. Shared Research Contract

- [x] 2.1 Create `isomer-labs-research-shared/SKILL.md` with truth-source order, durable artifact vocabulary, handoff expectations, evidence boundaries, and validation discipline.
- [x] 2.2 Add source-term mapping guidance from DeepScientist terms to Isomer Labs concepts, including Research Thread, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Decision Record, Gate, Provenance Record, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Coordination Policy, Capability Binding, and Execution Adapter.
- [x] 2.3 Add `yet-to-be-determined` guidance for unsettled concrete paths, filenames, command surfaces, runtime APIs, storage roots, runner homes, prompt injection mechanisms, paper-search providers, and generated artifact layouts.
- [x] 2.4 Add continuation mapping guidance: do not port DeepScientist `continuation_policy`, `auto_continue`, or `wait_for_user_or_resume`; express retained behavior as Agent Team Instance advancement, pause waiting for Operator Agent instruction, Workflow Stage recommendation, Gate, Decision Record, Completion Watcher Contract, or Signal Observation.
- [x] 2.5 Verify the shared skill uses only `name` and `description` in YAML frontmatter.

## 3. Core Stage Skills

- [x] 3.1 Extract `isomer-labs-research-intake` from `intake-audit` analysis.
- [x] 3.2 Extract `isomer-labs-research-scout` from `scout` analysis.
- [x] 3.3 Extract `isomer-labs-research-baseline` from `baseline` analysis.
- [x] 3.4 Extract `isomer-labs-research-idea` from `idea` analysis.
- [x] 3.5 Extract `isomer-labs-research-optimize` from `optimize` analysis.
- [x] 3.6 Extract `isomer-labs-research-experiment` from `experiment` analysis.
- [x] 3.7 Extract `isomer-labs-research-analysis` from `analysis-campaign` analysis.
- [x] 3.8 Extract `isomer-labs-research-decision` from `decision` analysis.
- [x] 3.9 Extract `isomer-labs-research-finalize` from `finalize` analysis.

## 4. Companion Skills

- [x] 4.1 Extract `isomer-labs-research-write` from `write` analysis.
- [x] 4.2 Extract `isomer-labs-research-review` from `review` analysis.
- [x] 4.3 Extract `isomer-labs-research-rebuttal` from `rebuttal` analysis.
- [x] 4.4 Extract `isomer-labs-research-paper-outline` from `paper-outline` analysis.
- [x] 4.5 Extract `isomer-labs-research-paper-plot` from `paper-plot` analysis.
- [x] 4.6 Extract `isomer-labs-research-figure-polish` from `figure-polish` analysis.
- [x] 4.7 Extract `isomer-labs-research-science` from `science` analysis.

## 5. References, Assets, and Progressive Disclosure

- [x] 5.1 Move long templates, checklists, and playbooks into one-level `references/` files for any skill whose `SKILL.md` would otherwise become too large.
- [x] 5.2 Copy required figure or plotting assets only when they directly support an extracted skill.
- [x] 5.3 Preserve applicable Apache 2.0 or upstream MIT license notices near copied or adapted assets, templates, scripts, or reference files.
- [x] 5.4 Ensure every reference file is directly linked from its parent `SKILL.md` with clear guidance on when to read it.

## 6. Generic Agent Mapping and Documentation

- [x] 6.1 Update `skillset/README.md` to point to `skillset/research-paradigm/` and explain the naming convention exception or extension.
- [x] 6.2 Update `teams/deepsci-org/source/team-design.md` to use generic research agents instead of DeepScientist-specific specialists.
- [x] 6.3 Map `research-lead`, `research-scout`, `research-designer`, `research-executor`, `research-writer`, and `research-reviewer` to their installed research-paradigm skills.
- [x] 6.4 Keep team topology, credentials, mailbox, and gateway details outside the skill bodies.

## 7. Validation

- [x] 7.1 Verify every `skillset/research-paradigm/isomer-labs-research-*/SKILL.md` exists.
- [x] 7.2 Validate each skill's YAML frontmatter contains `name` and `description`.
- [x] 7.3 Search the research-paradigm skillset for `DeepScientist`, `artifact.`, `memory.`, `bash_exec`, `DeepXiv`, `quest`, `worktree`, `workspace_mode`, `continuation_policy`, `auto_continue`, `wait_for_user_or_resume`, and `Houmao`, then confirm remaining matches are provenance, adaptation notes, explicit mappings, or explicit rejection notes.
- [x] 7.4 Search the research-paradigm skillset for concrete DeepScientist-style paths, runner homes, command wrappers, and API calls, then confirm unsettled equivalents are marked `yet-to-be-determined`.
- [x] 7.5 Compare extracted skills against `context/explore/deepscientist-skill-analysis/` and confirm each required purpose, exit criterion, durable output, and key pitfall is represented.
- [x] 7.6 Run `openspec status --change "extract-research-paradigm-skills"` and confirm the change remains apply-ready.
