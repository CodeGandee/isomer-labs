# isomer-op-toolbox-mgr-skill Specification

## Purpose
TBD - created by archiving change create-toolbox-creator-system-skill. Update Purpose after archive.
## Requirements
### Requirement: Toolbox Manager Skill Is Packaged Operator Guidance
The system SHALL provide `isomer-op-toolbox-mgr` as a packaged operator skill for creating and managing project-local Toolboxes through existing Isomer Toolbox, callback, runtime-param, and path-safety surfaces.

#### Scenario: Manager skill asset exists
- **WHEN** packaged operator system skills are inspected
- **THEN** `operator/isomer-op-toolbox-mgr/SKILL.md` exists
- **AND** its frontmatter `name` is `isomer-op-toolbox-mgr`

#### Scenario: Creator skill asset is not active
- **WHEN** packaged operator system skills are inspected
- **THEN** `operator/isomer-op-toolbox-creator` is not listed as an active packaged skill path
- **AND** no packaged alias folder for `isomer-op-toolbox-creator` is required

#### Scenario: Manager naming matches responsibility
- **WHEN** the skill instructions and UI metadata are inspected
- **THEN** the title, frontmatter, display name, default prompt, help output, and operator catalog identify the skill as `isomer-op-toolbox-mgr`
- **AND** they describe creation as one part of broader Toolbox management

#### Scenario: Skill uses Toolbox domain language
- **WHEN** the skill instructions are inspected
- **THEN** they use canonical terms for Toolbox, Toolbox ID, Callback Insertion Point, Toolbox-Local Key, Runtime Param, and Toolbox Scope
- **AND** they do not introduce legacy extension names as active user-facing terms

#### Scenario: Skill scope is system guidance
- **WHEN** the skill describes its authority
- **THEN** it states that Toolbox schema, callback registry semantics, runtime-param resolution, and CLI command behavior are owned by the existing Isomer surfaces
- **AND** it does not claim authority to bypass CLI validation or packaged system-skill ownership

### Requirement: Toolbox Manager Skill Selects Bounded Subcommands
The skill SHALL route each invocation to one bounded subcommand and load only the selected reference page before executing subcommand-specific work.

#### Scenario: Procedural subcommands are available
- **WHEN** the skill subcommand table is inspected
- **THEN** it lists `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`
- **AND** each procedural subcommand links to a reference page

#### Scenario: Helper subcommands are grouped by target resource
- **WHEN** the skill helper subcommand table is inspected
- **THEN** it lists `author-toolbox-source`, `edit-callback-declarations`, `edit-runtime-params`, and `inspect-effective-state`
- **AND** CRUD-style operations for the same Toolbox source, callback declaration, runtime-param material, or effective state are grouped under that helper instead of split into separate helper subcommands

#### Scenario: Help is the default empty invocation
- **WHEN** the skill is invoked without a concrete Toolbox task
- **THEN** it selects a help or orientation path
- **AND** it does not mutate Toolbox files, callback registries, Project Manifests, or Topic Workspace Manifests

### Requirement: Toolbox Manager Skill Preserves Toolbox Command Surface
The rename SHALL preserve the existing Toolbox lifecycle command surface while changing the owning skill identity.

#### Scenario: Procedural subcommands remain available
- **WHEN** the manager skill subcommand table is inspected
- **THEN** it lists `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`
- **AND** each procedural subcommand links to a local command page

#### Scenario: Helper subcommands remain grouped
- **WHEN** the manager skill helper table is inspected
- **THEN** it lists `author-toolbox-source`, `edit-callback-declarations`, `edit-runtime-params`, and `inspect-effective-state`
- **AND** CRUD-style operations for the same target resource remain grouped instead of split into separate helper subcommands

#### Scenario: Behavior stays CLI-backed
- **WHEN** the manager skill describes validation, install, callback refresh, Runtime Param mutation, or effective-state inspection
- **THEN** it continues to use existing `isomer-cli project toolboxes`, `project skill-callbacks`, and `project toolbox-params` command families
- **AND** it does not introduce new CLI or schema behavior

### Requirement: Toolbox Manager Skill Authors Project-Local Toolbox Source
The skill SHALL create or update Toolbox source material only in project-local Toolbox source locations unless the user explicitly supplies an allowed source path.

#### Scenario: New Toolbox source uses standard layout
- **WHEN** the user asks the skill to author a new Toolbox
- **THEN** the skill prepares source under `skillset/toolboxes/<toolbox-id>/`
- **AND** the source includes a Toolbox manifest, callback instruction material when callbacks are requested, runtime-param bundle files when defaults are requested, and a README or equivalent operator note when useful

#### Scenario: Callback declarations use Toolbox namespacing
- **WHEN** the skill drafts or edits Toolbox callback declarations
- **THEN** each callback uses a toolbox-local `key`
- **AND** the skill reports the installed callback id as `<toolbox_id>:<toolbox-local-key>`

#### Scenario: Runtime params keep local key shape
- **WHEN** the skill drafts or edits runtime-param declarations or bundles
- **THEN** it keeps `toolbox_id` and toolbox-local `key` separate in authored material
- **AND** it reports effective runtime-param ids as `<toolbox_id>:<param-key>`

#### Scenario: Unsafe source path is blocked
- **WHEN** the requested Toolbox source path is outside the Project root and no explicit allowance applies
- **THEN** the skill reports a blocker instead of writing files

### Requirement: Toolbox Manager Skill Uses Existing CLI Operations
The skill SHALL use existing `isomer-cli` command families for Toolbox validation, installation, callback refresh, runtime-param mutation, and effective-state inspection.

#### Scenario: Install uses Toolbox command surface
- **WHEN** the user asks to install or refresh a full Toolbox bundle
- **THEN** the skill uses or instructs `isomer-cli project toolboxes install --toolbox-dir <path>` with the selected scope
- **AND** it reports Toolbox id, source path, scope, installed callbacks, runtime-param import status, diagnostics, and effective status

#### Scenario: Callback-only refresh uses callback command surface
- **WHEN** the user asks for lower-level callback refresh without full Toolbox bundle installation
- **THEN** the skill uses or instructs the `isomer-cli project skill-callbacks` Toolbox install primitive
- **AND** it explains that this path is for migration, repair, test setup, or not-yet-fully-orchestrated bundle workflows

#### Scenario: Runtime params use toolbox-params command surface
- **WHEN** the user asks to set, unset, import, get, explain, or validate Toolbox runtime params
- **THEN** the skill uses or instructs `isomer-cli project toolbox-params` commands with Project, Research Topic, Topic Actor, or Topic Agent selectors as needed
- **AND** it uses `--topic-agent` for Topic Agent selection

#### Scenario: Effective state inspection is read-only
- **WHEN** the user asks to inspect callbacks, runtime params, Toolbox registration, gating, or diagnostics
- **THEN** the skill uses read-only CLI inspection commands unless the user explicitly requests mutation

### Requirement: Toolbox Manager Skill Preserves Safety and Output Contracts
The skill SHALL report concise Essential Output by default, provide Complete Output on request, and preserve Isomer safety constraints for scope, secrets, validation, and rollback.

#### Scenario: Essential Output is concise
- **WHEN** the skill completes a Toolbox authoring, conversion, insertion, runtime-param, management, or inspection task
- **THEN** the default chat output includes status, Toolbox id, Toolbox source path when relevant, selected scope, important files or ids, validation result, blockers, and next action

#### Scenario: Complete Output is available
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the skill includes grouped details such as command logs, mutation summary, authored paths, manifest entries, callback ids, runtime-param rows, diagnostics, rollback hints, and skipped work

#### Scenario: Project-wide scope is explicit
- **WHEN** a Toolbox operation targets Project scope or could affect every compatible topic context
- **THEN** the skill reports that scope explicitly before or with the operation result
- **AND** it warns when disable, uninstall, or source replacement could change callback behavior broadly

#### Scenario: Secret-like material is not authored
- **WHEN** user-provided Toolbox content appears to contain credentials, tokens, passwords, or other secret-like values
- **THEN** the skill reports a blocker or redacted diagnostic instead of writing the secret-like value into Toolbox source, manifest rows, callback material, or runtime-param bundles

### Requirement: Toolbox Manager Defaults Toolbox Skills to Routed or Manual Invocation
The Toolbox Manager skill SHALL author and describe Toolbox skills as routed or manually invoked surfaces by default, not as implicitly auto-invoked skills.

#### Scenario: Source scaffolding includes non-implicit metadata
- **WHEN** `isomer-op-toolbox-mgr` authors a Toolbox skill directory with `SKILL.md`
- **THEN** it also authors or recommends `agents/openai.yaml`
- **AND** that metadata sets `policy.allow_implicit_invocation` to `false`

#### Scenario: Default prompt names routed and manual use
- **WHEN** Toolbox Manager scaffolds or documents `agents/openai.yaml` for a Toolbox skill
- **THEN** the default prompt says to use the skill when routed by a Toolbox callback prompt or manually invoked for its named purpose
- **AND** it does not describe ordinary implicit auto-invocation as the default behavior

#### Scenario: Prompt-file router is preferred
- **WHEN** Toolbox Manager authors a callback that should apply a Toolbox skill subcommand
- **THEN** it prefers a short prompt-file callback that names the installed Toolbox skill, subcommand, and purpose
- **AND** it keeps reusable behavior in the Toolbox skill subcommand rather than duplicating it in the callback prompt

#### Scenario: Skill-directory callback is explicit exception
- **WHEN** Toolbox Manager uses a `skill_dir` callback source
- **THEN** it labels that source as supplemental instruction material
- **AND** it does not claim that registering the source automatically executes or implicitly invokes that skill

### Requirement: Toolbox Manager Conversion Preserves Invocation Boundary
The Toolbox Manager skill SHALL preserve the routed/manual invocation boundary when converting existing skill material into Toolbox material.

#### Scenario: Converted skill is not treated as automatic
- **WHEN** `convert-skill` converts an existing skill into Toolbox source
- **THEN** the converted Toolbox skill metadata disables implicit invocation by default
- **AND** callback declarations route to it through explicit prompt text unless the user chooses direct supplemental skill-directory material

#### Scenario: Converted callback reports invocation posture
- **WHEN** `convert-skill`, `author-toolbox`, or `insert-callback` reports created callback material
- **THEN** Essential Output includes whether the Toolbox skill is routed by prompt, manually invokable, or used as direct supplemental instruction material

