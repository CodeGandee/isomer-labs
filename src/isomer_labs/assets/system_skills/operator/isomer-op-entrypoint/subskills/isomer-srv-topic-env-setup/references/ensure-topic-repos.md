# Ensure Topic Repos

Use this subcommand to reuse verified registered repositories or orchestrate missing repository acquisition through the acting user or agent's external command surface. A new durable repository becomes a Canonical External Repository only after source and immutable-identity verification succeeds and `project repos register <repo-label> --path <existing-path>` records its non-main `topic.repos.<group...>.<repo-name>` binding with `storage_profile = "topic_repo"`. Under `isomer-default.v1`, the read-only candidate path is `<topic-workspace-dir>/repos/extern/...`.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `semantic_paths`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Source gate or target spec summary | Require the extracted source gate summary from `read-env-gate` and the repository requirements from `derive-env-gate`, including runnable target, desired commands, success criteria, repo hints, branch or commit and feature needs, projection access intent, dependency hints, and blockers. Refuse to run if both are missing, and tell the user to run `read-env-gate` and `derive-env-gate` first. |
| Repo semantic label and target | For each required repository, select a valid non-main `topic.repos.*` label. Query `project paths get` for an existing binding; otherwise query `project paths default` for a read-only candidate unless the user or target spec gives another safe Project-local target. Do not create a binding or directory during target planning. |
| Repository source and command procedure | Accept a URL, local path, provider ref, package source, repo name, or exact user-supplied clone, fetch, checkout, sparse, partial, submodule, LFS, local-copy, provider-CLI, credential-wrapper, or multi-command procedure. Exact user commands take priority. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace` and source gate summary from `read-env-gate`.
2. **Identify required repos**:
   - Use the source gate, target spec, desired commands, repo URLs, package names, import paths, build instructions, README references, projection access intent, and common project files already present at resolved `topic.repos.*` paths.
3. **Find registered repositories first**:
   - Query the semantic label through `project paths get` and require existing identity or provenance evidence from the caller or applicable typed Artifact.
   - Treat the repository as read-only by default for this subcommand. Do not infer source identity from the path or run source mutation merely to make it match the gate.
4. **Plan an unregistered target without mutation**:
   - Query `project paths default <label>` for the `isomer-default.v1` candidate, or preserve the user's safe explicit Project-local target.
   - Confirm the target is not already bound to another semantic label and record that no successful registration exists yet.
5. **Select the external procedure**:
   - Use the user's exact repository commands when supplied, subject to authorization and safety limits.
   - Otherwise select source-appropriate external commands from the requested locator, revision, authentication posture, repository features, target spec, resource limits, and inspection needs. Do not impose a mandatory history depth, remote name, provider, staging layout, retry sequence, or cleanup policy.
   - Record the method rationale and relevant non-secret options before execution.
6. **Run commands outside Isomer**:
   - Execute the selected clone, fetch, checkout, sparse, partial, submodule, LFS, copy, provider, or wrapper procedure through the ordinary user or agent command surface.
   - Do not translate it into an `isomer-cli` command, Service Request, Execution Adapter Command Request, or generic Isomer `argv` passthrough.
7. **Infer or search for missing sources when needed**:
   - When a required repo is absent and the gate implies runnable repo code but gives no explicit source, infer or search for a likely source.
   - Present ambiguity for selection or record a blocker before command execution. Acquire only a source whose relationship can be verified.
8. **Warning-label inferred sources**:
   - For every repository acquired from an inferred or discovered source, record the repo name, candidate target, inferred source, reason for choosing it, and uncertainty or review needed.
9. **Verify before registration**:
   - Through external source-specific checks, verify the requested and resolved locators, intended source relationship, target path, immutable commit or digest, branch or selected revision, required repository features, and access posture.
   - If acquisition or verification fails, leaves partial content, or produces an unexpected identity, do not register it. Preserve the external content, record sanitized attempt and filesystem posture, impact, blockers, and safe resume condition, and stop.
10. **Register verified topology**:
   - Run `isomer-cli --print-json project repos register <repo-label> --path <existing-target>` only after verification succeeds.
   - On a label or path conflict, leave both targets untouched and report registration as incomplete.
11. **Record provenance and inspect repo contents**:
   - Record or link the semantic label, requested and resolved locators, immutable identity, selected external method, sanitized command evidence, observation time, access and license posture, relationship basis, limitations, blockers, and provenance refs in the applicable typed Artifact owner.
   - Check files such as `README*`, `pyproject.toml`, `setup.py`, `requirements*.txt`, `environment.yml`, `package.json`, `pnpm-lock.yaml`, `CMakeLists.txt`, `Cargo.toml`, `Makefile`, CUDA files, shell scripts, notebooks, and test commands.
12. **Report repo context**:
   - Stop with blockers when a missing required repo source remains ambiguous, an externally acquired repository cannot be verified against the desired command, registration fails, Artifact recording fails, or an existing repo is unsuitable. A successful path binding without required provenance remains incomplete readiness.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, parent guardrails, and user request, then execute the plan.

## External Repository Rules

- Exact user-supplied repository commands take priority. Examples in this skill are illustrative and replaceable.
- When selecting commands, account for branch or commit selection, sparse or partial checkout, submodules, LFS, provider-specific behavior, authentication, local sources, history needs, and resource limits.
- Later fetch, pull, checkout, repair, feature, or history operations against an already registered repository remain external user or agent commands. Record a new immutable Artifact revision when the observed identity changes; keep the semantic path stable.
- Keep the manifest binding compact: `label`, `path`, and `storage_profile`. Do not infer `storage_profile` from a directory name, and do not treat default-looking paths as registered storage without a semantic label.
- Do not place task repos in the Project root, Agent Workspace, `.pixi/`, `tmp/`, or other disposable directories as the durable repo location.
- Do not claim readiness just because a repo exists; repo checks must still be represented in `topic.env.topic_setup_target_spec` and verified later.
- Do not ask Isomer to clean, repair, move, or remove partial external content. The user or acting agent decides whether to inspect, resume, move, or remove it under the applicable authorization.
- Do not persist credentials, signed query strings, authorization headers, environment secrets, credential-helper output, or raw stdout or stderr. Preserve only redacted descriptions, tool class, relevant non-secret options, status, and observed immutable identity.

## Output Notes

Carry forward:

- repo name;
- semantic label;
- expected path;
- path source for the repository;
- registration command evidence when a new `topic.repos.*` label was registered;
- requested and resolved source;
- user-supplied or agent-selected external method, non-secret options, and selection rationale;
- external verification evidence and observed immutable commit or digest;
- partial-result posture, impact, and safe resume condition when incomplete;
- access, license, relationship, limitation, blocker, and provenance refs;
- source warning, if any;
- projection access intent, if the target spec says the repo must be visible from topic-main;
- relevant files inspected;
- likely dependency signals;
- likely verification commands;
- blockers.
