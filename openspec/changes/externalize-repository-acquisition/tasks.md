## 1. Add Non-Executing Repository Target and Registration Surfaces

- [ ] 1.1 Extend Workspace Path Resolution so `project paths default` accepts a valid unregistered non-main `topic.repos.<group...>.<repo-name>` label and returns its `isomer-default.v1` `repos/extern/...` candidate with `storage_profile = "topic_repo"` without writing a manifest, Path Plan, directory, or file.
- [ ] 1.2 Add a core `project repos register <repo-label> --path <existing-path>` handler that normalizes bare labels, requires a safe existing directory, fixes the profile to `topic_repo`, delegates to Topic Workspace Manifest registration, and never creates content or invokes a subprocess.
- [ ] 1.3 Register the new command in the core Project command tree with stable text and `--print-json` output, explicit mutation posture, and diagnostics for invalid labels, main-repository misuse, missing paths, non-directories, unsafe paths, and binding conflicts.
- [ ] 1.4 Update `project repos create`, `project paths default`, and related CLI help and example metadata to distinguish directory creation, read-only target planning, and existing-path registration and to state that none initializes or acquires a Git repository.
- [ ] 1.5 Add Workspace Path Resolution unit tests for dynamic grouped-repository defaults, grouped-label validation, custom Topic Workspace paths, explicit target independence, deterministic output, and proof that the default query creates no binding or filesystem content.
- [ ] 1.6 Add CLI and handler tests for successful existing-directory registration, label normalization, manifest output, idempotent same-path posture, conflict rejection, missing and non-directory rejection, `topic.repos.main` rejection, no implicit replacement, and absence of subprocess execution.

## 2. Remove the Isomer Repository Acquisition API

- [ ] 2.1 Remove `project repos acquire` from `src/isomer_labs/cli/commands/kaoju_project.py`, including its options, help, service factory, imports, and any CLI example or command-coverage declaration.
- [ ] 2.2 Delete `src/isomer_labs/kaoju/repositories.py` and remove all package exports, type references, helper functions, error mappings, and tests whose subject is the fixed clone, deepen, verification, staging, move, or cleanup service.
- [ ] 2.3 Remove `repository_acquisition` from the Research Operation Extension Point registry and update execution-adapter tests so package mutation, smoke, trial, document-build, and viewer operations remain unchanged.
- [ ] 2.4 Ensure no replacement Isomer service accepts repository `argv`, shell text, provider names, clone options, credentials, retry policy, or cleanup policy, and add an architecture assertion that repository registration does not depend on `ExecutionAdapterCommandRequest`.
- [ ] 2.5 Update CLI help snapshots and command-discovery tests to require `project repos register`, reject `project repos acquire`, and prove that invoking the removed command fails through the normal unknown-command path without an alias or fallback.

## 3. Refactor Kaoju Repository Identity and Provenance

- [ ] 3.1 Refactor canonical-repository content validation so it consumes the registered semantic label and caller-observed immutable identity, performs only non-executing filesystem and payload checks, and never invokes Git or fabricates an acquisition command request.
- [ ] 3.2 Define and validate the repository fields used by `KAOJU:ASSOCIATED-SOURCE-CODE`, `KAOJU:ARTIFACT-LIBRARY`, and applicable provenance records for requested and resolved locators, semantic label, immutable commit or digest, acquisition method, sanitized command evidence, observation time, access, license, relationship basis, limitations, and blockers.
- [ ] 3.3 Add redaction coverage for credential-bearing URLs, signed query strings, headers, environment values, credential-helper output, stdout, and stderr so durable repository evidence preserves useful non-secret observations without storing secrets.
- [ ] 3.4 Replace Kaoju integration acquisition setup with deterministic test-owned external Git commands followed by `project repos register` and typed Artifact operations, keeping the Git commands outside Isomer service assertions.
- [ ] 3.5 Add integration scenarios for successful acquire-verify-register-record ordering, source-identity mismatch, partial external checkout, registration conflict after successful acquisition, Artifact failure after valid topology registration, and later revision recording at a stable semantic path.
- [ ] 3.6 Update code-trial prerequisite tests to consume a verified registered source ref and immutable identity without asserting a `repository_acquisition` extension request, while preserving environment, smoke, Gate, trial, and result behavior.

## 4. Rewrite Packaged System-Skill Guidance

- [ ] 4.1 Rewrite the Kaoju `ingest-source-code` command page and `isomer-kaoju-acquire` workflow to query or choose a candidate target, honor user-supplied commands, select external commands only when needed, verify identity externally, register the existing path, and record typed Artifacts in order.
- [ ] 4.2 Update `isomer-kaoju-shared`, workspace, examine, trial, and other consuming Kaoju guidance so registered semantic labels and observed immutable identity are the durable inputs and no procedure expects an Isomer-generated repository command request.
- [ ] 4.3 Update the Kaoju family README and packaged research-paradigm overview to remove the depth-one canonical policy, place repository execution outside Execution Adapter operations, and explain the topology-versus-provenance boundary.
- [ ] 4.4 Rewrite `isomer-srv-topic-env-setup` and its references so gate derivation records candidate semantic targets, user-supplied or agent-selected external commands, verification evidence, post-success registration, partial-result posture, and readiness blockers without assigning Git execution or cleanup to Isomer.
- [ ] 4.5 Update topic creator, topic manager, topic team specialization, and every other operator or service reference that delegates repository setup so it preserves the external-command boundary and requires verified registration evidence from topic environment setup.
- [ ] 4.6 Update acquisition-decision output fields and examples to describe the actually selected external method and immutable result without imposing shallow-clone defaults, and keep credential-bearing command material out of skill-requested durable output.
- [ ] 4.7 Verify the `skillset/` symlink projections expose the changed package-owned files without creating a divergent source copy, then scan every manifest-listed packaged skill for active acquisition ownership drift.

## 5. Enforce the Boundary in Skill Validation

- [ ] 5.1 Add a package-wide system-skill validation rule that rejects active `project repos acquire`, `repository_acquisition`, removed Kaoju repository-service references, Isomer-owned Git execution, Isomer-owned partial-checkout cleanup, and registration-before-verification guidance with file and line diagnostics.
- [ ] 5.2 Update Kaoju family validation to accept authorized direct repository commands as external operations while continuing to reject unregistered executable paths for Isomer-owned mutations and preserving all existing artifact, owner, Gate, environment, paper, wiki, and procedure checks.
- [ ] 5.3 Add valid fixtures for exact user commands, agent-selected Git commands, provider CLI use, local-copy acquisition, branch or commit selection, sparse or partial checkout, submodules, LFS, external verification, semantic registration, and typed provenance recording.
- [ ] 5.4 Add invalid fixtures for the removed command and extension point, generic Isomer `argv` passthrough, a fixed mandatory depth-one sequence, pre-verification binding, fabricated command requests, secret-bearing durable evidence, and claims that Isomer cleans partial external content.
- [ ] 5.5 Extend packaged-skill and materialization tests to run the repository-boundary validation against the complete core and Kaoju groups and confirm source-mirrored symlink projections cannot hide stale active guidance.

## 6. Update Public and Developer Documentation

- [ ] 6.1 Replace the `project repos acquire` section in `docs/manual/cli-reference.md` with read-only dynamic target lookup and non-executing `project repos register` coverage, including prerequisites, exact side effects, text and JSON posture, failures, and a customizable external-command example.
- [ ] 6.2 Update `docs/tutorial/quickstart.md`, `docs/developer/packaged-system-skills.md`, the Kaoju documentation, and related architecture prose so repository acquisition is user-controlled or agent-controlled external work and only registration and durable records are Isomer operations.
- [ ] 6.3 Rewrite `docs/tutorial/prepare-topic-environment.md` to demonstrate candidate target lookup, replaceable external Git or provider commands, source and immutable-identity verification, post-acquisition registration, provenance, projection readiness, and explicit blocker handling.
- [ ] 6.4 Update any Topic Workspace, storage, external projection, setup, troubleshooting, or testing documentation that implies registration precedes acquisition, a fixed clone policy is canonical, or Isomer owns repository cleanup.
- [ ] 6.5 Extend `scripts/validate_docs.py` and its unit fixtures to reject the removed command, extension point, acquisition service, fixed Isomer clone promises, pre-verification registration, and Isomer cleanup claims while accepting correctly framed direct external commands.
- [ ] 6.6 Add a breaking-change entry to `CHANGELOG.md` that names the removed CLI command and extension point, introduces `project repos register`, and shows the external acquire-verify-register-record migration sequence.

## 7. Complete Regression and Distribution Coverage

- [ ] 7.1 Run targeted Workspace Path Resolution, Project CLI, Kaoju Artifact, code-trial, system-skill asset, research-paradigm validator, package validator, and documentation validator tests and resolve every change-related failure.
- [ ] 7.2 Run `pixi run validate-research-skills`, the full system-skill validation command, and `pixi run docs-validate` against the package-owned assets and their `skillset/` projections.
- [ ] 7.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, recording unrelated pre-existing failures separately and fixing every failure caused by this change.
- [ ] 7.4 Build and inspect the distributable package to confirm the removed repository service is absent, the new CLI surface and updated skills and docs are included, and installed Kaoju workflows do not depend on a repository checkout.
- [ ] 7.5 Search all active source, tests, docs, package assets, generated CLI examples, and built-package content for `project repos acquire`, `repository_acquisition`, `KaojuRepositoryService`, fixed canonical shallow-clone wording, and pre-verification registration; allow hits only in historical OpenSpec archives or an explicit changelog migration note.
