# research-paradigm-skills Specification

## Purpose
Define the reusable Isomer Labs research-paradigm skillset, including portable
research-stage skills, shared evidence vocabulary, generic agent mappings,
provenance handling, and validation rules that prevent DeepScientist runtime
coupling from becoming an Isomer requirement.

## Requirements
### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable research-paradigm skillset under `skillset/research-paradigm/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention.

#### Scenario: Core skill folders exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared` and core research skill folders for intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science

#### Scenario: Skill frontmatter is valid
- **WHEN** each extracted skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields, and the `name` field matches the `isomer-rsch-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** its `SKILL.md` and directly linked references do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

### Requirement: Generic Research Vocabulary
The extracted skills SHALL describe portable research behavior using established Isomer Labs concepts and without requiring DeepScientist workspace APIs or DeepScientist-specific runtime surfaces.

#### Scenario: DeepScientist API terms are mapped to Isomer concepts
- **WHEN** an extracted skill describes artifacts, memory, terminal execution, paper search, or execution isolation
- **THEN** it uses Isomer concepts such as Research Thread, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Decision Record, Gate, Provenance Record, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Capability Binding, Coordination Policy, and Execution Adapter

#### Scenario: Source-specific terms are bounded
- **WHEN** an extracted skill mentions a source-specific term such as DeepScientist, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, quest, branch, worktree, `workspace_mode`, `continuation_policy`, `auto_continue`, or `wait_for_user_or_resume`
- **THEN** the mention is limited to provenance, adaptation notes, or an explicit mapping, and is not a required runtime operation

#### Scenario: Continuation policy is not ported
- **WHEN** an extracted skill preserves DeepScientist behavior about continuing, pausing, resuming, or monitoring long-running work
- **THEN** it describes the behavior through Agent Team Instance advancement under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage recommendations, Gates, Decision Records, Completion Watcher Contracts, or Signal Observations, and does not require an Isomer `continuation_policy` field

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark unsettled concrete paths, filenames, commands, runtime APIs, storage roots, and generated artifact layouts as `yet-to-be-determined` instead of guessing them.

#### Scenario: Path is not settled
- **WHEN** a DeepScientist source skill uses a concrete path or filename and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Runtime API is not settled
- **WHEN** a DeepScientist source skill depends on a command, tool wrapper, artifact API, memory API, runner home, prompt injection mechanism, or paper-search provider with no settled Isomer equivalent
- **THEN** the extracted skill marks that surface as `yet-to-be-determined` and avoids inventing an implementation-specific default

### Requirement: Shared Research Contract
The skillset SHALL include a shared research contract skill that defines common evidence, artifact, handoff, and validation rules for all research-stage skills.

#### Scenario: Shared contract covers common surfaces
- **WHEN** `isomer-rsch-shared/SKILL.md` is inspected
- **THEN** it defines truth-source order, Isomer concept mapping, durable Artifact vocabulary, handoff expectations, claim and evidence boundaries, source provenance, `yet-to-be-determined` handling, and validation discipline

#### Scenario: Stage skills reference shared rules
- **WHEN** a stage or companion skill needs common research discipline
- **THEN** it references the shared research contract instead of duplicating long common instructions

### Requirement: DeepScientist Methodology Preservation
The extracted skills SHALL preserve the reusable research-stage logic summarized in `context/explore/deepscientist-skill-analysis/`.

#### Scenario: Stage gate behavior is preserved
- **WHEN** a stage skill is inspected
- **THEN** it includes the corresponding stage purpose, entry signals, exit criteria, durable outputs, and key pitfalls from the DeepScientist skill analysis

#### Scenario: Companion behavior is preserved
- **WHEN** a companion skill such as review, rebuttal, paper-outline, paper-plot, figure-polish, or science is inspected
- **THEN** it includes the companion's bounded purpose, expected inputs, durable outputs, and validation rules

### Requirement: Progressive Disclosure
The skillset SHALL keep skill entrypoints concise and move long reusable detail into one-level reference files.

#### Scenario: Long methodology detail is moved to references
- **WHEN** a skill needs templates, checklists, long playbooks, or examples
- **THEN** the skill stores them under that skill's `references/`, `assets/`, or `scripts/` directory and links them directly from `SKILL.md`

#### Scenario: No extraneous documentation is added
- **WHEN** a skill folder is inspected
- **THEN** it contains only files that directly support skill use, such as `SKILL.md`, `agents/openai.yaml`, `references/`, `assets/`, or `scripts/`

### Requirement: Generic Agent Mapping
The team documentation SHALL map generic research agents to the extracted `isomer-rsch-*` skills without making the skills depend on one team topology.

#### Scenario: Generic role map exists
- **WHEN** the updated team documentation is inspected
- **THEN** it defines generic research roles and lists the `isomer-rsch-*` research-paradigm skills installed for each role

#### Scenario: Skill bundles are topology-neutral
- **WHEN** an extracted skill is inspected
- **THEN** it does not require a specific Houmao specialist name, mailbox route, gateway, credential, or agent topology to perform its research operation

### Requirement: Provenance and Licensing
The implementation SHALL preserve source provenance and license notices for copied or adapted DeepScientist-derived material.

#### Scenario: Copied materials include license notices
- **WHEN** source text, templates, scripts, assets, or reference files are copied or materially adapted from DeepScientist or upstream helper skills
- **THEN** the new skillset includes the applicable Apache 2.0 or upstream MIT notice in a nearby license or provenance file

#### Scenario: Source analysis remains traceable
- **WHEN** a reviewer wants to trace an extracted skill back to its source behavior
- **THEN** the skill or its references identify the source analysis file or DeepScientist source skill used during extraction

### Requirement: Validation
The implementation SHALL include validation steps that check skill structure, naming consistency, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a `SKILL.md`, valid frontmatter, and expected supporting resources

#### Scenario: Naming validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every renamed skill folder, `SKILL.md` frontmatter `name:`, manifest default prompt, and active role mapping uses `isomer-rsch-*`

#### Scenario: Coupling validation runs
- **WHEN** the implementation is complete
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including continuation scheduling terms, and confirms any remaining matches are provenance or mapping text only

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the implementation is complete
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined`
