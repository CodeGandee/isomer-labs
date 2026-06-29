# Ensure Topic Repos

Use this subcommand to ensure independent repos required by the source gate exist under the resolved topic repository root. When a repo becomes a durable topic repository, register it through Workspace Path Resolution as a `topic.repos.*` label with `storage_profile = "topic_repo"`; prefer `project repos create` or `project paths register` over manual `topic-workspace.toml` edits.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `semantic_paths`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Source gate summary | Require the extracted source gate summary from `read-env-gate`, including runnable target, desired commands, success criteria, repo hints, dependency hints, and blockers. Refuse to run if it is missing, and tell the user to run `read-env-gate` first. |
| `repos_root` | Use the resolved topic repository root from semantic path evidence; under `isomer-default.v1` this is normally `<topic-workspace-dir>/repos/` for independent setup repos. Create it only when this step needs to materialize or inspect required repos, and record the semantic label and path source. |
| Explicit repo source | Optional. Use a URL, local path, package source, or repo name from the prompt or source gate only when the expected repo path is missing. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-topic-workspace` and source gate summary from `read-env-gate`.
2. **Identify required repos** from the source gate, desired commands, repo URLs, package names, import paths, build instructions, README references, and common project files already present under the resolved topic repository root.
3. **Use the required repo root**. Place every independent repo under the resolved topic repository root. Create that root when needed and safe.
4. **Find existing repos first**. If the expected repo already exists under `repos/<repo-name>`, treat it as read-only for this subcommand: inspect it, record evidence, and do not run `git pull`, `git checkout`, copy files into it, delete files from it, install packages into it, regenerate files in it, or otherwise mutate it.
5. **Acquire explicit sources only when missing**. When a required repo is absent and the gate or prompt provides a URL, local path, or package source, first register the target through `project repos create <repo-label>` or `project paths register topic.repos.<group...>.<repo-name> --storage-profile topic_repo`, then clone, copy, or materialize it at the resolved path.
6. **Infer or search for missing repos when needed**. When a required repo is absent and the gate implies runnable repo code but gives no explicit source, infer or search for a likely source. Acquire it only when it can be plausibly matched to the desired target.
7. **Warning-label inferred sources**. For every repo acquired from an inferred or discovered source, record the repo name, expected path, inferred source, reason for choosing it, and uncertainty or review needed.
8. **Inspect repo contents** for dependency and command signals, such as `README*`, `pyproject.toml`, `setup.py`, `requirements*.txt`, `environment.yml`, `package.json`, `pnpm-lock.yaml`, `CMakeLists.txt`, `Cargo.toml`, `Makefile`, CUDA files, shell scripts, notebooks, and test commands.
9. **Report repo context**. Stop with blockers when a missing required repo source remains too ambiguous, an acquired repo cannot be verified against the desired command, or an existing repo is unsuitable.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, parent guardrails, and user request, then execute the plan.

## Acquisition Rules

- Use `git clone <source> <resolved-repos-root>/<repo-name>` for Git sources only when `<resolved-repos-root>/<repo-name>` does not already exist.
- Copy or link local sources only when `<resolved-repos-root>/<repo-name>` does not already exist and the user or gate clearly authorizes that source.
- Keep the manifest binding compact: `label`, `path`, and `storage_profile`. Do not infer `storage_profile` from a directory name, and do not treat default-looking paths as registered storage without a semantic label.
- Do not place task repos in the Project root, Agent Workspace, `.pixi/`, `tmp/`, or other disposable directories as the durable repo location.
- Do not claim readiness just because a repo exists; repo checks must still be represented in `topic.env.topic_setup_target_spec` and verified later.
- Do not mutate an existing repo to make it match the gate. If an existing repo is the wrong source, wrong branch, dirty, missing files, or otherwise unsuitable, report a blocker and explain what user action or explicit authorization is needed.

## Output Notes

Carry forward:

- repo name;
- expected path;
- semantic label and path source for the repo root;
- binding command evidence when a new `topic.repos.*` label was registered;
- explicit or inferred source;
- source warning, if any;
- relevant files inspected;
- likely dependency signals;
- likely verification commands;
- blockers.
