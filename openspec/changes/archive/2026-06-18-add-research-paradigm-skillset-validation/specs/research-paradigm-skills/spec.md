## MODIFIED Requirements

### Requirement: Validation
The implementation SHALL include a repository-runnable validation harness that checks skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, stale terminology, resolved TBD placeholders, local reference integrity, manifest consistency, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level references

#### Scenario: Naming validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms every skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-rsch-*` names consistently

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the validation harness inspects an enriched `SKILL.md`
- **THEN** validation confirms it has a near-top `## Workflow`, numbered workflow steps, concise reference routing, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: Coupling validation runs
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including artifact APIs, memory APIs, command wrappers, provider names, workspace terms, continuation scheduling terms, and concrete source paths, and confirms any remaining matches are provenance, adaptation notes, explicit mappings, deferred-resource notes, or explicit rejection notes

#### Scenario: Placeholder registry validation runs
- **WHEN** the validation harness finds a `[[tbd-surface:<id>]]` placeholder in active research-paradigm skill text
- **THEN** validation confirms the placeholder id is listed in a directly linked TBD registry and is not one of the resolved workspace, recording, lifecycle, CLI topic-context, or execution-extension placeholder ids

#### Scenario: Self-containment validation runs
- **WHEN** the validation harness inspects enriched skill entrypoints and linked references
- **THEN** validation confirms they do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined` or represented by registered unresolved TBD-surface placeholders

#### Scenario: Repository command runs the harness
- **WHEN** a developer or agent runs the repository skillset validation command
- **THEN** the command validates `skillset/research-paradigm`, prints deterministic diagnostics as `path:line: code message`, and exits nonzero when validation errors exist

#### Scenario: Whole bundle validation surface is scanned
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation inspects every Markdown and YAML file in the subtree and classifies files or sections by role before applying strict checks or rule-specific allow zones

#### Scenario: Allow zones preserve explanatory mapping text
- **WHEN** stale source terms, former TBD ids, or source-runtime names appear inside configured provenance files, license notices, deferred-resource notes, source-term mapping sections, rejected-runtime sections, or resolved-surface mapping tables
- **THEN** validation allows those occurrences only for the matching rule and continues to reject the same terms when they appear as active skill guidance

#### Scenario: Stale lifecycle and workspace terms are reported
- **WHEN** active research-paradigm skill text uses Research Goal, Research Thread, Research Branch, or Isomer Workspace as current Isomer domain terms
- **THEN** validation reports the stale term and directs the skill text to use Research Topic, Research Inquiry, Research Inquiry Relationship, or Topic Workspace

#### Scenario: Resolved workspace path TBDs are reported
- **WHEN** active research-paradigm skill text emits an ordinary workspace path TBD placeholder such as `[[tbd-surface:path-topic-workspace]]`, `[[tbd-surface:path-agent-workspace]]`, `[[tbd-surface:path-run-logs]]`, `[[tbd-surface:path-experiment-output]]`, `[[tbd-surface:path-analysis-output]]`, `[[tbd-surface:path-paper-layout]]`, or `[[tbd-surface:path-figure-output]]`
- **THEN** validation reports the placeholder as resolved and directs the skill text to use Workspace Path Resolution, semantic workspace scopes, or semantic Artifact kinds

#### Scenario: Unregistered TBD surface is reported
- **WHEN** active research-paradigm skill text emits a `[[tbd-surface:<id>]]` placeholder whose id is absent from the directly linked TBD registry
- **THEN** validation reports the unregistered id and identifies the file and line that emitted it

#### Scenario: Shared TBD registry is canonical
- **WHEN** the validation harness validates `[[tbd-surface:<id>]]` placeholders or resolved former IDs anywhere in the research-paradigm subtree
- **THEN** validation treats `isomer-rsch-shared/references/tbd-surface-registry.md` as the canonical registry for the subtree

#### Scenario: Local TBD registry mirror drift is reported
- **WHEN** a directly loaded local contract file contains a `## TBD Surface Registry` mirror section
- **THEN** validation confirms the local mirror has exact resolved-ID coverage and normalized resolution text matching the shared registry, and reports missing IDs, extra IDs, or changed resolution meaning

#### Scenario: Hard-coded local and source-analysis paths are reported
- **WHEN** active research-paradigm skill text depends on local absolute paths, source-analysis paths, archived OpenSpec change paths, `extern/orphan` paths, DeepScientist runtime paths, or concrete runner homes outside an allowed provenance or deferred-resource zone
- **THEN** validation reports the hard-coded path and directs the skill text to use self-contained references, accepted Isomer contracts, or registered unresolved TBD-surface placeholders

#### Scenario: Broken local reference is reported
- **WHEN** a `SKILL.md` references a local `references/`, `assets/`, or `scripts/` path that does not exist inside the same skill directory
- **THEN** validation reports the broken reference with the referring `SKILL.md` file and line

#### Scenario: Manifest mismatch is reported
- **WHEN** a skill's `agents/openai.yaml` `interface.display_name` does not equal the skill folder and `SKILL.md` frontmatter name, or `interface.default_prompt` does not invoke the same `$isomer-rsch-*` skill
- **THEN** validation reports the manifest mismatch and identifies the affected manifest field
