## MODIFIED Requirements

### Requirement: DeepScientist Methodology Preservation
The extracted skills SHALL preserve reusable research-stage logic from the corresponding DeepScientist source skill directories, including source `SKILL.md` content and directly supporting source references, templates, scripts, or assets when those materials contain portable research method.

#### Scenario: Stage gate behavior is preserved
- **WHEN** a stage skill is inspected
- **THEN** it includes the corresponding stage purpose, entry signals, exit criteria, route taxonomy, durable outputs, key pitfalls, and source-derived gates needed to perform the stage without reading DeepScientist source files

#### Scenario: Companion behavior is preserved
- **WHEN** a companion skill such as review, rebuttal, paper-outline, paper-plot, figure-polish, or science is inspected
- **THEN** it includes the companion's bounded purpose, expected inputs, durable outputs, validation rules, source-derived templates or examples, and handoff behavior needed to perform the companion task without reading DeepScientist source files

#### Scenario: Rich source details are preserved locally
- **WHEN** a source skill contains reusable route taxonomies, playbooks, templates, checklists, examples, boundary cases, failure handling, or operational guidance
- **THEN** the extracted skill preserves that detail in its `SKILL.md`, local `references/`, local `assets/`, or local `scripts/`, or records an explicit implementation rationale for deferring the detail

#### Scenario: Source concepts are translated correctly
- **WHEN** preserved source material mentions DeepScientist-specific concepts such as quest, artifact operations, memory operations, command wrappers, literature providers, workspace paths, branch/worktree assumptions, continuation scheduling, or generated artifact layouts
- **THEN** the extracted skill maps the concept to accepted Isomer terms, marks unsettled concrete surfaces with `[[tbd-surface:<id>]]`, or confines the source term to provenance or explicit mapping text

### Requirement: Progressive Disclosure
The skillset SHALL keep skill entrypoints concise, move long reusable detail into one-level local resources, and avoid active dependencies on files outside the skill bundle.

#### Scenario: Long methodology detail is moved to references
- **WHEN** a skill needs templates, checklists, long playbooks, route examples, operational notes, or boundary cases
- **THEN** the skill stores them under that skill's `references/`, `assets/`, or `scripts/` directory and links every entrypoint-needed file directly from `SKILL.md`

#### Scenario: Active skill bundle is self-contained
- **WHEN** an enriched skill's active `SKILL.md` and directly linked references are inspected
- **THEN** they do not require `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, local absolute paths, or other files outside that skill's directory to execute the skill

#### Scenario: Source provenance remains traceable
- **WHEN** source text, templates, scripts, assets, or reference files are copied or materially adapted
- **THEN** the target skill includes nearby provenance that identifies the DeepScientist source skill and applicable license context without making the source tree a runtime dependency

#### Scenario: Scripts and assets are sanitized before import
- **WHEN** source scripts or assets are imported into an enriched skill
- **THEN** they are directly useful for the skill and do not contain source-local user paths, demo-output defaults, private paths, unsatisfied hard dependencies, or DeepScientist runtime assumptions as active behavior

#### Scenario: No extraneous documentation is added
- **WHEN** a skill folder is inspected
- **THEN** it contains only files that directly support skill use, such as `SKILL.md`, `agents/openai.yaml`, `references/`, `assets/`, or `scripts/`

### Requirement: Validation
The implementation SHALL include validation steps that check skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level references

#### Scenario: Naming validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-rsch-*` names consistently

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the implementation is complete
- **THEN** validation confirms every enriched `SKILL.md` has a near-top `## Workflow`, numbered workflow steps, concise references to detailed sections, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: Coupling validation runs
- **WHEN** the implementation is complete
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including artifact APIs, memory APIs, command wrappers, provider names, workspace terms, continuation scheduling terms, and concrete source paths, and confirms any remaining matches are provenance, adaptation notes, explicit mappings, or explicit rejection notes

#### Scenario: Placeholder registry validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every `[[tbd-surface:<id>]]` used by the enriched skills is listed in a directly linked TBD registry or is replaced with an existing registered placeholder

#### Scenario: Self-containment validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms enriched skill entrypoints and linked references do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

## ADDED Requirements

### Requirement: Imsight Workflow Entrypoints
Each enriched `isomer-rsch-*` skill SHALL use the Imsight skill-entrypoint structure for its `SKILL.md` while preserving the skill's trigger behavior and research guardrails.

#### Scenario: Workflow section is near the top
- **WHEN** an enriched `SKILL.md` is inspected
- **THEN** it has a near-top `## Workflow` section before detailed procedure, contract, guardrail, or reference sections

#### Scenario: Workflow steps are actionable and concise
- **WHEN** an enriched `## Workflow` section is inspected
- **THEN** it uses numbered steps that name the action to take and point to detailed sections or local references rather than embedding long procedures inline

#### Scenario: Workflow includes freeform fallback
- **WHEN** an enriched `## Workflow` section is inspected
- **THEN** it tells the agent to use its native planning tool to build and execute a step-by-step plan from the skill's constraints, references, and user request when the task does not map cleanly to the default steps

#### Scenario: Reference routing is explicit
- **WHEN** an enriched skill has local references
- **THEN** its entrypoint states which references to read first and which references to read for route-specific, template-specific, operational, validation, or writing-facing needs

### Requirement: Parallelized Skill Enrichment
The implementation SHALL use subagents to parallelize enrichment work across disjoint skill folders and centralize integration and validation in the main agent.

#### Scenario: Worker scopes are disjoint
- **WHEN** subagents are launched for implementation
- **THEN** each subagent receives an explicit non-overlapping write scope and instructions not to revert or overwrite unrelated edits from other workers

#### Scenario: Source and target context is provided
- **WHEN** a subagent enriches a skill folder
- **THEN** it is directed to inspect the target skill, `isomer-rsch-analysis`, the corresponding DeepScientist source skill directory, the migration contract, the shared TBD registry, and the Imsight formatting guidance before editing

#### Scenario: Main agent integrates shared files
- **WHEN** subagents complete their assigned work
- **THEN** the main agent reviews and integrates their changes, owns shared files such as the TBD registry and suite README, resolves conflicts, and runs final validation

#### Scenario: Large resources are bounded
- **WHEN** a source skill contains large generated catalogs, plotting scripts, style assets, or venue templates
- **THEN** the implementation either imports sanitized directly useful resources in the assigned skill folder or records a deferred task for a follow-up resource-focused change
