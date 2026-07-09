# user-skill-callbacks Specification

## Purpose
TBD - created by archiving change add-user-skill-callbacks. Update Purpose after archive.
## Requirements
### Requirement: User Skill Callback Contract
The system SHALL define User Skill Callback as user-provided instruction material attached to a system skill name and a callback stage, separate from provider-backed Research Operation Extension Points and separate from packaged system skill ownership.

#### Scenario: Callback record has stable identity
- **WHEN** a User Skill Callback is registered
- **THEN** the stored record includes a stable callback id, target system skill name, callback stage, callback source, callback scope, status, priority, and source location metadata

#### Scenario: Supported stages are bounded
- **WHEN** a user registers or resolves a User Skill Callback
- **THEN** validation accepts only the `begin` and `end` callback stages in the initial version

#### Scenario: Unsupported stage is rejected
- **WHEN** a user requests a callback stage other than `begin` or `end`
- **THEN** the system rejects the request with a deterministic diagnostic that names the unsupported stage

#### Scenario: Callback is instruction material
- **WHEN** a User Skill Callback is resolved for a system skill
- **THEN** the result is treated as supplemental instruction material for the current skill workflow and not as executable provider payload, runtime state, credential material, or an override of packaged skill ownership

#### Scenario: Missing callbacks are empty success
- **WHEN** no active User Skill Callback matches the requested system skill and stage
- **THEN** resolution succeeds with an empty callback list and does not block the owning skill workflow

### Requirement: Callback Source Types
The system SHALL support User Skill Callback sources from one inline prompt, one prompt file, or one external skill directory per callback record.

#### Scenario: Inline prompt is registered
- **WHEN** a user registers a callback with inline prompt text
- **THEN** the system materializes the prompt as managed callback content and stores a registry record that points to that managed content rather than embedding large prompt bodies in the registry ref field

#### Scenario: Prompt file is registered
- **WHEN** a user registers a callback with a prompt file path
- **THEN** validation confirms the file exists, is readable, is not a directory, and resolves according to the callback path policy before storing the registry record

#### Scenario: External skill directory is registered
- **WHEN** a user registers a callback with a skill directory path
- **THEN** validation confirms the directory contains `SKILL.md` and records the directory as supplemental instruction material without installing it as a packaged system skill

#### Scenario: Source kind is exclusive
- **WHEN** a registration request provides multiple source kinds or no source kind
- **THEN** the system rejects the request with a deterministic diagnostic that requires exactly one of inline prompt, prompt file, or skill directory

#### Scenario: External paths are explicit
- **WHEN** a callback source path resolves outside the Project root
- **THEN** the system accepts it only when the command explicitly allows an external callback source and reports the external source in validation or resolution output

#### Scenario: Secret-like callback input is rejected
- **WHEN** callback registry metadata or inline prompt material contains an inline credential, token, API key, password, or other secret-like value detected by project validation
- **THEN** validation rejects the callback record or managed prompt content without printing the secret value in diagnostics

### Requirement: Callback Registry Storage
The system SHALL store User Skill Callback registrations in declarative registry files referenced by Project or topic configuration rather than in packaged system skill files.

#### Scenario: Registry has schema version
- **WHEN** a User Skill Callback registry file is loaded
- **THEN** validation requires a supported registry schema version and deterministic callback entry fields

#### Scenario: Project registry ref is declarative
- **WHEN** a Project Manifest declares a User Skill Callback registry ref
- **THEN** the system treats the ref as project-scoped instruction customization and validates the referenced registry before project-scoped callback commands depend on it

#### Scenario: Topic registry ref is declarative
- **WHEN** a Research Topic Config declares a User Skill Callback registry ref
- **THEN** the system treats the ref as topic-scoped instruction customization and validates the referenced registry before topic-scoped callback commands depend on it

#### Scenario: Registry does not mutate system skills
- **WHEN** a callback is registered, disabled, or validated
- **THEN** the system does not edit packaged system skill directories, `SKILL.md` files, or the system skill manifest as part of callback registry mutation

#### Scenario: Disabled callback is retained but inactive
- **WHEN** a callback record is disabled
- **THEN** the registry retains the record for auditability, marks it inactive, and excludes it from normal resolution results

### Requirement: Callback CLI Surface
The system SHALL expose a generic `isomer-cli project skill-callbacks` command group for User Skill Callback management, resolution, and lower-level callback-material operations that are not necessarily installed as full Toolbox bundles.

#### Scenario: Register command creates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks register` with a target system skill, supported stage, scope, and exactly one source kind
- **THEN** the command validates the inputs, creates or updates the appropriate callback registry, and reports the callback id, target skill, stage, scope, status, and source summary

#### Scenario: Register command supports loose callback material
- **WHEN** a user has callback material that is not packaged as a Toolbox manifest
- **THEN** the `register` command provides the direct mutation path for prompt, prompt-file, or skill-directory callback sources

#### Scenario: Install command is a callback-manifest primitive
- **WHEN** a user runs the lower-level callback-manifest install operation for a Toolbox directory
- **THEN** the command installs or refreshes callback records from the Toolbox manifest without being the canonical high-level Toolbox bundle install surface

#### Scenario: Resolve command is read-only
- **WHEN** a user runs `isomer-cli project skill-callbacks resolve` for a system skill and callback stage
- **THEN** the command loads the selected Project and Effective Topic Context, returns the active callbacks in deterministic order, and does not mutate registry files or callback content

#### Scenario: List command summarizes callbacks
- **WHEN** a user runs `isomer-cli project skill-callbacks list`
- **THEN** the command lists callback ids, target skills, stages, scopes, statuses, priorities, and source summaries visible from the selected Project or topic context

#### Scenario: Show command displays one callback
- **WHEN** a user runs `isomer-cli project skill-callbacks show <callback-id>`
- **THEN** the command displays the matching callback metadata and source reference while preserving redaction rules for secret-like material

#### Scenario: Disable command deactivates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks disable <callback-id>`
- **THEN** the command marks the callback inactive in its registry and reports the previous and new status

#### Scenario: Validate command checks registries
- **WHEN** a user runs `isomer-cli project skill-callbacks validate`
- **THEN** the command validates reachable callback registries, source paths, target system skill names, stages, duplicate active ids, status values, priority values, and redaction-sensitive fields

### Requirement: Callback Resolution and Merge Order
The system SHALL resolve User Skill Callbacks deterministically from the active Project and topic context before a participating skill applies them through explicit owning-skill workflow steps.

#### Scenario: Exact skill and stage match
- **WHEN** callbacks are resolved for a participating system skill
- **THEN** resolution includes only active callback records whose target system skill name and callback stage match the requested skill and stage

#### Scenario: Scope precedence is deterministic
- **WHEN** both project-scoped and topic-scoped callbacks match the requested skill and stage
- **THEN** resolution orders the more specific topic-scoped callbacks ahead of project-scoped callbacks unless an accepted registry priority rule orders callbacks within the same scope

#### Scenario: Priority order is deterministic
- **WHEN** multiple active callbacks match within the same scope
- **THEN** resolution sorts them by configured priority and then by stable callback id as the tie breaker

#### Scenario: Resolve output includes diagnostics
- **WHEN** callback resolution skips an inactive callback, rejects a malformed callback, or observes a missing optional registry
- **THEN** the result includes deterministic diagnostics without treating unrelated invalid callback records as successful instruction material

#### Scenario: Begin stage applies before workflow work
- **WHEN** a participating skill resolves `begin` callbacks
- **THEN** the skill applies the resolved instructions from an explicit numbered workflow step after mandatory skill identity and context checks and before the first skill-specific workflow action

#### Scenario: End stage applies before completion
- **WHEN** a participating skill resolves `end` callbacks
- **THEN** the skill applies the resolved instructions from an explicit numbered workflow step after producing tentative workflow outputs and before final response, handoff, or marking the top-level workflow complete

#### Scenario: Callback resolution is not implicit hook injection
- **WHEN** a participating skill documents callback participation
- **THEN** callback resolution is described as explicit workflow work owned by that skill
- **AND** the system does not rely on ambient reminder prose or implicit hook injection to make agents run callbacks

### Requirement: Callback Authority and Safety
The system SHALL preserve system, developer, owning-skill, current user request, and Isomer domain constraints when applying User Skill Callbacks.

#### Scenario: Callback cannot override higher-priority constraints
- **WHEN** callback instruction material conflicts with system policy, developer instructions, the owning system skill's required guardrails, or accepted Isomer domain constraints
- **THEN** the participating skill follows the higher-priority constraint and reports the callback conflict when it affects the workflow

#### Scenario: Callback cannot replace current user intent
- **WHEN** callback instruction material conflicts with the current user request for the invocation
- **THEN** the participating skill treats the current user request as the active user intent unless the current user explicitly asks to use the registered callback behavior

#### Scenario: Callback does not execute external skill directory automatically
- **WHEN** a callback source is an external skill directory
- **THEN** the participating skill reads the directory's `SKILL.md` as supplemental instructions but does not treat that directory as an installed system skill or execute scripts from it solely because it was registered as a callback

#### Scenario: Callback cannot bypass gates
- **WHEN** callback instructions ask the agent to bypass required Gates, validation steps, recording obligations, or permission checks
- **THEN** the participating skill refuses the bypass and continues through the owning workflow's required controls

### Requirement: Callback Keys Support Toolbox Namespaces
The system SHALL accept callback ids that include a Toolbox namespace separator so installed Toolbox callbacks can use `<toolbox_id>:<toolbox-local-key>` as their stable callback key.

#### Scenario: Namespaced callback key is valid
- **WHEN** callback validation sees an installed callback key in the form `<toolbox_id>:<toolbox-local-key>`
- **THEN** validation accepts exactly one colon namespace separator when the Toolbox id and toolbox-local key otherwise use valid callback key characters

#### Scenario: Toolbox-local part cannot contain colon
- **WHEN** callback validation sees an installed callback key whose toolbox-local key part contains `:`
- **THEN** validation rejects the callback key with a deterministic diagnostic

#### Scenario: Duplicate active namespaced keys are rejected
- **WHEN** two active callback records visible to a Project or Research Topic context use the same installed callback key
- **THEN** validation rejects the duplicate active callback key with a deterministic diagnostic

#### Scenario: Distinct namespaced keys coexist on one extension point
- **WHEN** two active callback records have the same target system skill name and callback stage but different installed callback keys
- **THEN** callback resolution includes both records

#### Scenario: Extension point does not overwrite callback identity
- **WHEN** a callback registration or Toolbox install writes a callback for a target system skill name and callback stage that already has another callback
- **THEN** the existing callback remains registered unless its installed callback key is the same as the new callback key

#### Scenario: Registry output preserves installed callback key
- **WHEN** the system lists, shows, resolves, disables, validates, or serializes a callback installed from a Toolbox manifest
- **THEN** the reported callback id is the installed callback key

#### Scenario: Toolbox metadata is optional for manual callbacks
- **WHEN** a callback is registered directly without a Toolbox manifest
- **THEN** the registry record does not require `toolbox_id` or toolbox-local callback key metadata

### Requirement: Toolbox Status Gates Toolbox-Installed Callbacks
The system SHALL honor effective Toolbox status when resolving callbacks installed from Toolbox manifests.

#### Scenario: Active Toolbox callback resolves normally
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected Project, Research Topic, Topic Actor, or Topic Agent context is `active`
- **THEN** callback resolution may include that callback when its target skill and stage match the request

#### Scenario: Disabled Toolbox callback is skipped
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected context is disabled
- **THEN** callback resolution excludes that callback without deleting or mutating the callback registry record

#### Scenario: Missing Toolbox registration blocks installed callback
- **WHEN** an active callback record has `toolbox_id` metadata but no applicable Toolbox registration exists
- **THEN** callback resolution excludes that callback with a deterministic diagnostic

#### Scenario: Disablement is context-specific
- **WHEN** a Toolbox is disabled for one Topic Actor or Topic Agent but remains enabled at the broader Research Topic or Project scope
- **THEN** callback resolution skips the Toolbox callbacks only for the disabled effective context and continues resolving them for other contexts where the Toolbox remains enabled

#### Scenario: Callback list explains Toolbox gating
- **WHEN** a callback list, resolve, show, or validate command reports Toolbox-installed callbacks
- **THEN** the output includes enough Toolbox status metadata to explain whether the callback is effective or gated off for the selected context

### Requirement: Callback Target Validation Uses Insertion Point Catalog
The system SHALL validate User Skill Callback target skill and stage pairs against manifest-declared callback insertion points.

#### Scenario: Declared insertion point is accepted
- **WHEN** a User Skill Callback targets a system skill and callback stage pair declared in the packaged callback insertion-point catalog
- **THEN** validation accepts the target pair subject to the existing registry, source, scope, status, priority, and redaction rules

#### Scenario: Undeclared insertion point is rejected
- **WHEN** a User Skill Callback targets a packaged system skill and stage pair that is not declared as a callback insertion point
- **THEN** validation rejects the target pair with a deterministic diagnostic that names the missing insertion point
- **AND** the diagnostic directs users toward callback insertion-point discovery

#### Scenario: Optional extension target remains catalog based
- **WHEN** a User Skill Callback targets an insertion point belonging to a known optional system extension
- **THEN** validation uses the packaged catalog declaration rather than attempting to inspect the Project operator filesystem
- **AND** command output can report whether the extension is Project-declared or only catalog-known

### Requirement: Toolbox Skill Routing Does Not Imply Automatic Invocation
User Skill Callback guidance SHALL keep Toolbox skill routing separate from automatic skill invocation.

#### Scenario: Prompt callback routes explicitly
- **WHEN** a callback prompt tells the active agent to invoke a Toolbox skill and subcommand
- **THEN** that instruction is treated as explicit supplemental routing under the active owning skill workflow
- **AND** the owning skill's callback application step, current user request, and higher-priority constraints remain authoritative

#### Scenario: Toolbox skill metadata can disable implicit invocation
- **WHEN** a Toolbox skill includes agent metadata with `policy.allow_implicit_invocation = false`
- **THEN** agent-host discovery should treat the skill as manually invoked or explicitly routed by instructions rather than as a normal implicit auto-selection candidate
- **AND** callback resolution still does not execute the skill automatically

