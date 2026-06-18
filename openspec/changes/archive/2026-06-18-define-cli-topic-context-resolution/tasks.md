## 1. Main Spec Alignment

- [x] 1.1 Create the main `cli-topic-context-resolution` spec from the delta spec, including Project discovery, Project Manifest topic registration, Research Topic Config TOML, Effective Topic Context, topic selection precedence, environment identity refs, validation, and CLI scope boundaries.
- [x] 1.2 Update the main `workspace-path-resolution` spec so Workspace Path Resolution can consume a validated Effective Topic Context without performing independent Research Topic selection.
- [x] 1.3 Update the main `research-recording-contracts` spec so Artifact Core Records stay generic and minimal, while Artifact Format Profiles and Artifact Extensions attach as optional records or refs.
- [x] 1.4 Confirm the main `research-lifecycle-state` spec remains the authority for Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, and Agent Team Instance lifecycle state.
- [x] 1.5 Confirm Research Recording Contracts remain the authority for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, and Gates without making topic-specific artifact formats mandatory core fields.

## 2. Architecture and Domain Language Updates

- [x] 2.1 Update architecture notes that describe `isomer-cli`, Project Manifest discovery, Topic Workspace discovery, topic-level configuration, or artifact customization to include Effective Topic Context, Research Topic Config, Artifact Format Profiles, and Artifact Extensions.
- [x] 2.2 Update `.imsight-arts/project-explore` domain language where needed so Project Manifest, Research Topic Config, Effective Topic Context, Artifact Core Record, Artifact Format Profile, Artifact Extension, Topic Workspace, and Workspace Runtime use current domain terms.
- [x] 2.3 Replace any touched stale active terms such as Research Thread or Isomer Workspace with Research Inquiry, Research Topic, or Topic Workspace as appropriate.
- [x] 2.4 Add example Project Manifest and Research Topic Config TOML fragments that show a registered Research Topic, Topic Workspace ref, Topic Agent Team Profile ref, Execution Adapter ref, Capability Binding refs, Gate policy refs, Artifact Format Profile refs, and Artifact Extension refs.

## 3. Research Skill Contract Updates

- [x] 3.1 Update `isomer-rsch-shared` guidance so skills can refer to `isomer-cli` Effective Topic Context when a CLI command needs topic-specific behavior.
- [x] 3.2 Update `isomer-rsch-shared` guidance so skills treat core Artifact records as generic and minimal and use optional Artifact Format Profile or Artifact Extension refs only for topic-specific output expectations.
- [x] 3.3 Update local `isomer-research-contract.md` copies only if they mention CLI topic selection, Project Manifest topic registration, topic-specific command behavior, or artifact format customization.
- [x] 3.4 Preserve `[[tbd-surface:api-execution-command]]`, `[[tbd-surface:policy-scheduler]]`, `[[tbd-surface:policy-cost-privacy-gate]]`, `[[tbd-surface:schema-skill-binding]]`, `[[tbd-surface:policy-baseline-waiver]]`, and `[[tbd-surface:provider-literature-search]]` as open placeholders.
- [x] 3.5 Confirm the shared TBD registry does not claim that CLI topic context resolution or artifact format customization settles command execution, scheduler policy, Skill Binding, credential binding, literature providers, baseline-waiver policy, cost/privacy Gate thresholds, or concrete validation/render commands.

## 4. Validation and Example Consistency

- [x] 4.1 Search docs and skills for unregistered topic-context environment variables and keep only the accepted identity refs and accepted Workspace Path Resolution path overrides.
- [x] 4.2 Search docs and skills for language that treats environment variables as durable truth and revise it to say resolved refs and paths must be recorded through Workspace Runtime or Provenance Records.
- [x] 4.3 Search docs and skills for language that makes Research Topic Config own Run status, command outputs, live process state, Artifacts, Evidence Items, Gates, Decision Records, or Provenance Records.
- [x] 4.4 Search docs and skills for language that makes Artifact Format Profiles or Artifact Extensions mandatory core Artifact fields.
- [x] 4.5 Verify topic-context and artifact-format examples do not store secrets, credentials, tokens, or provider-specific command implementations inline.

## 5. Final Review

- [x] 5.1 Run `openspec validate define-cli-topic-context-resolution`.
- [x] 5.2 Run `openspec validate cli-topic-context-resolution`, `openspec validate workspace-path-resolution`, and `openspec validate research-recording-contracts` after main specs are synced.
- [x] 5.3 Run `openspec validate research-lifecycle-state`, `openspec validate research-recording-contracts`, and `openspec validate research-paradigm-skills` after related references are updated.
- [x] 5.4 Confirm unknown or missing Artifact Format Profiles and Artifact Extensions degrade to generic Artifact handling in the documented contract.
- [x] 5.5 Run `git diff --check`.
- [x] 5.6 Review the final diff for accidental implementation of command runners, scheduler loops, credential storage, Skill Binding schemas, provider-specific APIs, or mandatory topic-specific Artifact schemas.
