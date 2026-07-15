## Why

`isomer-cli project repos acquire` hard-codes one Git acquisition strategy inside the Isomer API, so it cannot honor user-selected commands or common repository workflows such as a selected branch or commit, sparse or partial clones, submodules, Git LFS, local sources, mirrors, provider CLIs, credential wrappers, and custom fetch sequences. Repository acquisition should remain an agent-controlled external operation, while Isomer should register the resulting Canonical External Repository and preserve its observed identity and provenance only after the requested commands succeed.

## What Changes

- **BREAKING** Remove `isomer-cli project repos acquire`, the Kaoju repository-acquisition service, and the `repository_acquisition` CLI execution point instead of retaining a fixed Git-command API.
- Require Kaoju and other applicable system skills to let the acting agent select and execute direct `git`, `gh`, provider, local-copy, or user-supplied commands outside `isomer-cli`, subject to the user request, applicable Gates, resource limits, and existing owner boundaries.
- Extend the read-only default-path query to unregistered non-main `topic.repos.*` labels and add `isomer-cli project repos register <repo-label> --path <existing-path>` as a non-executing post-acquisition registration flow; neither surface creates, clones, fetches, checks out, rewrites, or deletes repository content.
- Keep topology registration separate from research provenance: the Topic Workspace Manifest records the semantic path, while Kaoju Artifacts record requested and observed source identity, immutable commit, acquisition method, command evidence, access and license posture, limitations, relationships, and blockers.
- Update Kaoju pipeline, acquire, examine, workspace, and shared guidance so repository selection and acquisition remain flexible, registration happens only after verification, and failures do not create successful repository bindings or evidence.
- Update CLI, skill, integration, validator, documentation, tutorial, and changelog coverage so no active instruction, help text, test, or public example retains the removed acquisition command or implies that Isomer owns Git execution.

## Capabilities

### New Capabilities

- `external-repository-registration`: Defines the platform boundary between agent-controlled repository acquisition and Isomer-owned semantic registration, identity recording, provenance, and failure posture.

### Modified Capabilities

- `workspace-path-resolution`: Define non-executing registration of an existing Canonical External Repository under a grouped `topic.repos.*` label and keep helper defaults distinct from acquisition.
- `kaoju-cli-services`: Remove the repository acquisition API and execution point while preserving deterministic Artifact, Run, Service Request, paper, wiki, and registration operations.
- `kaoju-code-execution`: Replace canonical CLI acquisition with prompt-sensitive external commands followed by verification and registration.
- `kaoju-survey-intents`: Require associated source code to be acquired externally and registered only after its identity and paper relationship are established.
- `kaoju-research-extension`: Clarify that repository command selection and execution belong to the acting agent, while Isomer owners retain path, registration, Gate, environment, and durable-record authority.
- `kaoju-artifact-bindings`: Require repository-related Artifacts to preserve the actual external acquisition method and observed identity without depending on a fabricated or CLI-internal acquisition request.
- `research-paradigm-skills`: Update packaged Kaoju guidance and validation so skills use direct, user-sensitive repository commands and then invoke non-executing Isomer registration surfaces.
- `packaged-system-skills`: Require every packaged system skill to keep repository command selection and execution outside Isomer APIs and validate the acquire-then-register ordering.
- `isomer-service-env-setup-skill`: Update gate-driven Topic Workspace setup so the acting agent runs repository commands directly, verifies their result, and registers the existing repository afterward.
- `topic-main-development-repository`: Clarify that a Canonical External Repository becomes part of Topic Workspace topology through semantic registration, not through an Isomer-owned Git acquisition service.
- `isomer-documentation-system-guide`: Update command reference, workflows, tutorials, side-effect descriptions, and documentation validation for the external-acquisition and post-registration boundary.
- `research-workflow-tutorial-suite`: Teach external repository acquisition, verification, and post-acquisition registration in the topic environment preparation tutorial.

## Impact

- Removes `src/isomer_labs/kaoju/repositories.py`, the `project repos acquire` command registration, its execution-point constant, related helpers, and acquisition-specific tests.
- Changes the public CLI surface and all active Kaoju, operator, service, and shared system-skill routes that currently name or imply Isomer-owned repository acquisition.
- Uses Workspace Path Resolution, the new non-executing `project repos register` helper, and typed Kaoju Artifact operations as the durable topology and provenance surfaces.
- Updates main OpenSpec contracts, packaged skill assets and their source mirrors when present, validation rules and fixtures, CLI/manual/developer/tutorial documentation, integration scenarios, and `CHANGELOG.md`.
- Does not change Topic Main Development Repository setup, code-trial execution, document builds, viewer launch, Service Requests, or other bounded execution-adapter operations.
