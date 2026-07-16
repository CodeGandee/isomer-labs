## Context

Kaoju currently routes source ingestion through `isomer-cli project repos acquire`. `KaojuRepositoryService.acquire()` constructs a fixed `git ls-remote`, depth-one `git clone`, optional deepen, `git rev-parse`, and `git fsck` sequence, dispatches those commands through the `repository_acquisition` Execution Adapter extension point, stages the checkout, and registers a semantic path only after its built-in checks pass. Packaged Kaoju guidance, integration tests, the CLI reference, tutorials, and developer documentation all present this route as the canonical way to obtain source code.

That API cannot represent the range of commands a user or repository may require. Common examples include a selected branch or commit, partial or sparse clones, mirrors, submodules, Git LFS, provider CLIs, local checkouts, credential wrappers, interactive authentication, custom remotes, archive or copy-based materialization, and multi-step recovery. Adding options for each case would keep source-control policy inside Isomer and would remain incomplete.

The existing platform already separates the two durable concerns that follow acquisition. The Topic Workspace Manifest owns semantic path topology, including non-main `topic.repos.<group...>.<repo-name>` bindings. Typed Kaoju Artifacts and Provenance Records own source identity, immutable revision, acquisition evidence, relationships, access posture, limitations, and research lineage. The design uses those owners directly and removes repository process execution from Isomer.

The Canonical External Repository term remains unchanged. Under the accepted domain language, it is a non-main topic repository resolved through a semantic label, with `repos/extern/<repo-label-path>` only as the `isomer-default.v1` helper layout. The semantic label, not the physical default directory, is its durable topology identity.

## Goals / Non-Goals

**Goals:**

- Remove fixed Git and provider command construction, dispatch, retry, staging, and cleanup from `isomer-cli` and Isomer package services.
- Let the acting user or agent use exact user-supplied commands or select task-appropriate external commands without an Isomer command-shape abstraction.
- Provide a non-mutating way to obtain the default target for an unregistered non-main `topic.repos.*` label.
- Provide a repository-specific, non-executing command that registers an existing verified directory through the Topic Workspace Manifest.
- Require acquisition, source verification, semantic registration, and research provenance recording in that order.
- Update every active Kaoju, service, operator, shared, documentation, validation, and test surface that currently assigns repository acquisition to Isomer.
- Preserve sanitized acquisition evidence and immutable source identity without storing credentials or sensitive raw output.
- Make the removal a clean break, with no deprecated alias, hidden fallback, command translation, or generic command passthrough.

**Non-Goals:**

- Define one replacement `git`, `gh`, provider, copy, authentication, checkout, retry, or cleanup procedure.
- Add an `argv`, script, shell, or provider-command parameter to an Isomer repository API.
- Make Isomer responsible for partial checkout cleanup, remote repair, credential management, or user shell configuration.
- Remove Git operations that Isomer performs for platform-owned Topic Main Development Repository or Agent Workspace worktree lifecycle. Those operations have a separate owner and are outside source acquisition for reading or research evidence.
- Change Canonical External Repository projection policy, Topic Main Repository ownership, code-trial execution, document builds, viewer launch, Service Requests, or other registered Execution Adapter operations.
- Store remote identity, command transcripts, credentials, license claims, or paper relationships in the Topic Workspace Manifest.
- Migrate existing valid semantic bindings or Artifact records solely because an older Isomer version performed their acquisition.

## Decisions

### Remove Repository Acquisition from the Isomer Execution Boundary

`project repos acquire`, `KaojuRepositoryService`, its `repositories.py` implementation, acquisition-specific CLI wiring, and the `repository_acquisition` extension-point identifier will be removed together. No deprecated command or compatibility alias will remain.

The replacement is not a generic Isomer command runner. When a user provides exact commands, the acting agent runs those commands through its ordinary terminal or tool surface within the accepted request and Gate. When the user provides only the desired source and outcome, the acting agent selects commands based on source type, revision, repository features, authentication posture, available tools, resource limits, and inspection needs. Isomer receives the resulting path and durable observations after those commands finish.

An alternative was to change `project repos acquire` to accept arbitrary `argv`, a shell script, or a provider name. That still makes Isomer the command dispatcher, complicates interactive and multi-command workflows, duplicates the agent's existing execution surface, and creates a credential-bearing API. It is rejected.

Another alternative was to keep the current fixed service and add branch, depth, sparse, submodule, LFS, and provider options. This expands the hard-coded policy without making it complete. It is also rejected.

### Separate Target Planning from Post-Acquisition Registration

A new repository starts with a non-mutating target decision:

1. If the semantic label already resolves, the acting agent uses the registered path subject to the requested operation and existing content posture.
2. If the label is new and the default layout is acceptable, `project paths default topic.repos.<group...>.<repo-name>` returns `<topic-workspace>/repos/extern/<group...>/<repo-name>` with `storage_profile = "topic_repo"` and `mutated: false`.
3. If the user or workspace plan requires another safe path, the acting agent uses that explicit target.

`default_semantic_path()` will recognize valid grouped non-main repository labels even when they are absent from the manifest. It will derive the path and profile without creating a binding, directory, Path Plan, or repository. Built-in label behavior remains unchanged.

After external acquisition and source verification, `isomer-cli project repos register <repo-label> --path <existing-path>` will normalize a bare repository label to `topic.repos.<group...>.<repo-name>`, require a safe existing directory, and register it with `storage_profile = "topic_repo"`. The handler will delegate to Workspace Path Resolution and Topic Workspace Manifest registration. It will not create the target or run a subprocess.

The registration command performs filesystem and path-safety validation only. It does not call Git to infer a remote, branch, commit, cleanliness, object connectivity, submodule state, or history depth. Those observations come from external commands selected by the acting user or agent.

`project paths register` remains the generic binding operation. `project repos register` adds repository-label normalization, the fixed topic-repository profile, existing-directory validation, and clearer public intent. `project repos create` remains a directory-and-binding helper and must state that it does not initialize or acquire a Git repository. Its `--no-create` form is not the acquisition workflow and packaged guidance must not use it to publish a successful binding before verification.

An alternative was to register the label before running external commands so the target could be resolved normally. A failed or ambiguous acquisition would then leave a successful-looking canonical binding. A read-only candidate query preserves semantic path planning without that false state, so pre-registration is rejected for acquisition workflows.

### Use an Acquire, Verify, Register, Record Sequence

Applicable system skills will teach one state sequence while leaving command bodies open:

```text
resolve source identity
        |
query or choose candidate target (read-only)
        |
run user-supplied or agent-selected external commands
        |
verify target, source relationship, and immutable identity externally
        |
register existing path under topic.repos.*
        |
record or revise typed Artifact and provenance state
```

No successful semantic binding or accepted repository Artifact is created when acquisition or identity verification fails. The skill records a blocker or Run checkpoint with the sanitized attempted method, observed filesystem posture, impact, and safe resume condition. Partial content remains outside Isomer ownership; the user or agent chooses whether to inspect, resume, move, or remove it.

If semantic registration fails after successful acquisition, the content also remains untouched. The procedure reports a registration blocker and can retry the manifest operation after resolving label or path conflicts. If Artifact recording fails after topology registration, the valid binding remains visible, but the research procedure stays incomplete and resumes at Artifact recording. The system does not roll back correct topology to simulate cross-store atomicity.

For an already registered repository, later fetch, pull, checkout, repair, submodule, LFS, or history commands follow the same external boundary. The path binding normally remains stable; a new immutable revision becomes a new or revised Artifact and Provenance Record rather than a silent rewrite of accepted history.

### Keep Topology, Source Identity, and Command Evidence in Their Existing Owners

The Topic Workspace Manifest stores only the semantic label, canonical path, storage profile, and existing manifest metadata. It does not become a repository metadata database.

When a research workflow accepts the repository, its typed Artifact and Provenance Records store or link:

- the semantic repository label;
- requested and resolved source locators;
- observed immutable commit or content digest;
- acquisition method and sanitized command evidence;
- verification time and observations;
- access and license posture;
- source-to-paper or source-to-reading-item relationship basis;
- limitations, staleness posture, blockers, and lineage refs.

Kaoju's canonical-repository content validation may check the registered path, caller-supplied identity syntax, and file-backed manifest integrity without executing Git. It must not infer identity by invoking a subprocess or fabricate a `repository_acquisition` command request. A `.git` directory, a `.git` indirection file, provider-specific metadata, or another externally verified source form must not force a hidden command sequence inside registration.

Command evidence is sanitized before durable recording. Credentials, signed query strings, authorization headers, environment secrets, credential-helper output, and sensitive raw stdout or stderr do not enter the Topic Workspace Manifest, Artifact payload, Run log, or diagnostic. The record preserves a redacted description, tool class, relevant non-secret options, result status, and observed immutable identity.

### Update System Skills by Ownership Layer

The implementation will update both packaged assets and any maintained source mirrors. The affected guidance includes Kaoju pipeline and acquisition pages, Kaoju shared and workspace procedure, topic environment setup, operator routes into topic setup, topic specialization setup references, family READMEs, and any active page found by repository-wide validation.

Kaoju retains research ownership for source discovery, relationship appraisal, command-method selection, source inspection, and evidence interpretation. Topic Workspace owners retain target planning, semantic registration, projections, Gates, and path validation. Kaoju Artifact services retain durable source identity and provenance. Environment mutation continues through Service Requests; code trials and other managed execution continue through their existing extension points.

Skills may show direct commands as illustrative examples, but they must identify them as user-controlled or agent-controlled external operations and must allow replacement by a user-supplied or repository-appropriate sequence. Active guidance must not imply that depth one, remote `origin`, one provider, or one cleanup strategy is canonical.

### Enforce the Boundary in Validation and Documentation

Package and research-skill validators will reject active references to `project repos acquire`, `repository_acquisition`, the removed Kaoju service, or an equivalent Isomer-owned repository command route. They will also reject acquisition flows that create a successful semantic binding before source verification. Direct `git`, provider, wrapper, and copy commands are valid for repository acquisition when nearby guidance identifies them as external, authorized, and followed by verification and registration.

Documentation validation will apply the same stale-surface checks to the CLI reference, tutorials, developer guides, packaged-skill descriptions, and examples. Public docs will distinguish:

| Operation | Owner | Isomer Mutation |
| --- | --- | --- |
| Candidate target query | Workspace Path Resolution | None |
| Clone, fetch, copy, checkout, repair, and source verification | Acting user or agent | None through Isomer |
| Existing-path semantic registration | Topic Workspace Manifest | Path binding only |
| Research source identity and provenance | Typed Artifact and Provenance operations | Durable research records |

The implementation will update CLI help and examples, Kaoju and service documentation, the topic environment tutorial, developer system-skill documentation, integration tests, and `CHANGELOG.md`. A repository-wide active-source scan must find no removed command or extension-point references outside historical OpenSpec archives or explicit migration notes.

### Keep Tests at the Ownership Boundaries

Workspace and CLI tests will cover unregistered dynamic default-path queries, non-mutating output, label normalization, existing-directory registration, path safety, binding conflicts, and the absence of subprocess calls. Kaoju tests will begin from repositories prepared by test fixtures with ordinary external Git commands, then call registration and Artifact operations separately.

Skill and documentation fixtures will cover user-supplied commands, agent-selected commands, non-default Git features, failed acquisition, failed verification, failed registration, redaction, and acquire-then-register ordering. Negative fixtures will prove that the old command, extension point, fixed shallow-clone promise, and pre-verification registration fail validation.

Tests may use Git directly to create deterministic local repositories. Their assertions must treat those commands as test setup rather than behavior emitted by the Isomer API.

## Risks / Trade-offs

- [Risk] Agents may choose unsafe or overly broad repository commands when no exact command is supplied. → Skills require source resolution, applicable Gates, resource checks, user constraints, bounded command selection, and visible command-method rationale before execution.
- [Risk] External commands can leave partial content that Isomer no longer stages or removes. → Failure output records the path posture and resume condition; cleanup requires an explicit user or agent decision under the same authorization.
- [Risk] A caller could register an existing directory that was not verified correctly. → Registration validates topology only, while skills and research acceptance require external identity evidence and typed provenance before reporting completion.
- [Risk] Manifest registration can succeed before Artifact recording, leaving an incomplete research procedure. → Keep the valid binding, checkpoint the incomplete stage, and retry the idempotent Artifact operation instead of attempting cross-store rollback.
- [Risk] Custom commands may expose credentials in logs or payloads. → Require pre-recording redaction and add fixtures for URLs, environment variables, headers, credential helpers, stdout, and stderr.
- [Risk] Direct command examples may become accidental policy. → Mark examples as replaceable, validate the user-supplied-command priority, and avoid declaring one clone depth, provider, remote, or history posture as canonical.
- [Risk] Stale installed skills may continue invoking the removed command. → Make CLI failure explicit, update all packaged and source-mirrored guidance in the same release, document the breaking change, and add active-source validation.
- [Trade-off] The acting agent performs more orchestration than one `project repos acquire` call. → The extra steps expose the real command and identity decisions and support repository-specific workflows without expanding Isomer's API indefinitely.

## Migration Plan

1. Extend non-mutating default-path resolution for valid unregistered non-main `topic.repos.*` labels and add focused path-resolution tests.
2. Add core `project repos register` CLI wiring and a non-executing handler that requires an existing safe directory, normalizes labels, delegates manifest registration, emits stable text and JSON, and never invokes subprocesses.
3. Remove `project repos acquire`, `KaojuRepositoryService`, `src/isomer_labs/kaoju/repositories.py`, repository-acquisition helpers and imports, and `repository_acquisition` from the execution-point registry without a compatibility alias.
4. Update canonical-repository Artifact validation and Kaoju ingestion orchestration so caller-observed identity, semantic label, sanitized external command evidence, and provenance are recorded without a CLI-internal command request.
5. Rewrite all active Kaoju, topic-environment, operator-routing, shared, and family guidance to use candidate query, external acquisition, external verification, semantic registration, and durable recording in order.
6. Add package-wide skill validation and fixtures for the external repository boundary, then update current valid fixtures and remove acquisition-service fixtures.
7. Update CLI help, examples, manual and developer guides, tutorials, system-skill documentation, release notes, and documentation validation rules.
8. Run targeted CLI, Workspace Path Resolution, Kaoju, integration, skill-validation, and documentation tests, followed by `pixi run lint`, `pixi run typecheck`, and `pixi run test`. Search active source and built package content for removed command and extension-point names.

This is a clean-break release. Rollback consists of reverting the complete implementation before dependent skills are distributed. There is no dual-command period or runtime adapter. Existing semantic bindings and Artifact records remain valid because their durable path and source identity models do not depend on which actor originally executed Git.

## Open Questions

None. The process boundary, command removal, target-query behavior, registration command, ordering, provenance owners, validation posture, and clean-break migration are fixed by this change.
