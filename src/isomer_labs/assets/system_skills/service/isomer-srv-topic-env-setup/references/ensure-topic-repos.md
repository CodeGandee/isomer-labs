# Ensure Topic Repos

Use this subcommand to ensure independent repos required by the source gate exist at resolved non-main `topic.repos.*` paths. When a repo becomes a durable topic repository, register it through Workspace Path Resolution as a `topic.repos.<group...>.<repo-name>` label with `storage_profile = "topic_repo"`; prefer `project repos create` or `project paths register` over manual `topic-workspace.toml` edits. Under `isomer-default.v1`, helper-created non-main repositories default under `<topic-workspace-dir>/repos/extern/...`.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `semantic_paths`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Source gate or target spec summary | Require the extracted source gate summary from `read-env-gate` and the repository requirements from `derive-env-gate`, including runnable target, desired commands, success criteria, repo hints, clone-depth decisions, projection access intent, dependency hints, and blockers. Refuse to run if both are missing, and tell the user to run `read-env-gate` and `derive-env-gate` first. |
| Repo semantic path | For each required repository, resolve or register a non-main `topic.repos.*` label. Under `isomer-default.v1`, `project repos create <repo-label>` creates the default target under `<topic-workspace-dir>/repos/extern/<repo-label-path>`. Create the resolved path only when this step needs to materialize or inspect that repo, and record the semantic label, path, and path source. |
| Explicit repo source | Optional. Use a URL, local path, package source, or repo name from the prompt or source gate only when the expected repo path is missing. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace` and source gate summary from `read-env-gate`.
2. **Identify required repos**:
   - Use the source gate, target spec, desired commands, repo URLs, package names, import paths, build instructions, README references, projection access intent, and common project files already present at resolved `topic.repos.*` paths.
3. **Decide Git acquisition mode**:
   - For each missing Git repo, decide whether the work needs full Git history or only a source snapshot.
   - Default to `clone_mode: shallow` with `clone_depth: 1`.
   - Use `clone_mode: full-history` only when the prompt, Research Topic, source gate, target spec, benchmark protocol, provenance need, bisect or debugging task, changelog analysis, branch comparison, tag traversal, or version-history requirement implies it.
   - Record clone mode, clone depth, and the evidence for the decision before acquiring the repo.
4. **Use semantic repo paths**. Place every independent repo at a resolved non-main `topic.repos.*` path. The default helper location is `repos/extern/<repo-label-path>`, but explicit safe manifest bindings remain valid.
5. **Find existing repos first**:
   - If the expected repo already exists at the resolved semantic path, treat it as read-only by default for this subcommand.
   - Inspect it and record evidence.
   - Do not run `git pull`, `git checkout`, copy files into it, delete files from it, install packages into it, regenerate files in it, or otherwise mutate it.
6. **Acquire explicit sources only when missing**:
   - When a required repo is absent and the gate or prompt provides a URL, local path, or package source, first register the target through `project repos create <repo-label>` or `project paths register topic.repos.<group...>.<repo-name> --storage-profile topic_repo`.
   - Then clone, copy, or materialize it at the resolved path.
7. **Infer or search for missing repos when needed**:
   - When a required repo is absent and the gate implies runnable repo code but gives no explicit source, infer or search for a likely source.
   - Acquire it only when it can be plausibly matched to the desired target.
8. **Warning-label inferred sources**:
   - For every repo acquired from an inferred or discovered source, record the repo name, expected path, inferred source, reason for choosing it, and uncertainty or review needed.
9. **Inspect repo contents** for dependency and command signals:
   - Check files such as `README*`, `pyproject.toml`, `setup.py`, `requirements*.txt`, `environment.yml`, `package.json`, `pnpm-lock.yaml`, `CMakeLists.txt`, `Cargo.toml`, `Makefile`, CUDA files, shell scripts, notebooks, and test commands.
10. **Report repo context**:
   - Stop with blockers when a missing required repo source remains too ambiguous, an acquired repo cannot be verified against the desired command, or an existing repo is unsuitable.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, parent guardrails, and user request, then execute the plan.

## Acquisition Rules

- Use `git clone --depth=1 <source> <resolved-topic-repo-path>` for Git sources by default when `<resolved-topic-repo-path>` does not already exist.
- Use `git clone <source> <resolved-topic-repo-path>` without `--depth=1` only when the recorded clone mode is `full-history` and the target spec or source context explains why history is required.
- If a shallow clone later proves insufficient, report a blocker or ask for explicit authorization before recloning or fetching additional history.
- Copy or link local sources only when `<resolved-topic-repo-path>` does not already exist and the user or gate clearly authorizes that source.
- Keep the manifest binding compact: `label`, `path`, and `storage_profile`. Do not infer `storage_profile` from a directory name, and do not treat default-looking paths as registered storage without a semantic label.
- Do not place task repos in the Project root, Agent Workspace, `.pixi/`, `tmp/`, or other disposable directories as the durable repo location.
- Do not claim readiness just because a repo exists; repo checks must still be represented in `topic.env.topic_setup_target_spec` and verified later.
- Do not mutate an existing repo to make it match the gate. If an existing repo is the wrong source, wrong branch, dirty, missing files, or otherwise unsuitable, report a blocker and explain what user action or explicit authorization is needed.

## Output Notes

Carry forward:

- repo name;
- semantic label;
- expected path;
- path source for the repository;
- binding command evidence when a new `topic.repos.*` label was registered;
- explicit or inferred source;
- clone mode, clone depth, and clone-mode evidence for Git sources;
- source warning, if any;
- projection access intent, if the target spec says the repo must be visible from topic-main;
- relevant files inspected;
- likely dependency signals;
- likely verification commands;
- blockers.
