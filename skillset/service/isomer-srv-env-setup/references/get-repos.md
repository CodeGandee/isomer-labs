# Get Repos

Use this subcommand to materialize independent repos required by the source gate under the Topic Workspace.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace` and source gate summary from `read-gate`.
2. **Identify required repos** from the source gate, desired commands, repo URLs, package names, import paths, build instructions, README references, and common project files already present under `<topic-workspace-dir>/repos/`.
3. **Use the required repo root**. Place every independent repo under `<topic-workspace-dir>/repos/<repo-name>`. Create `<topic-workspace-dir>/repos/` when needed.
4. **Find existing repos first**. If the expected repo already exists under `repos/<repo-name>`, inspect it rather than downloading another copy.
5. **Acquire explicit sources**. When the gate or prompt provides a URL, local path, or package source, clone, copy, or materialize it under `repos/<repo-name>`.
6. **Infer or search when needed**. When the gate implies runnable repo code but gives no explicit source, infer or search for a likely source. Acquire it only when it can be plausibly matched to the desired target.
7. **Warning-label inferred sources**. For every repo acquired from an inferred or discovered source, record the repo name, expected path, inferred source, reason for choosing it, and uncertainty or review needed.
8. **Inspect repo contents** for dependency and command signals, such as `README*`, `pyproject.toml`, `setup.py`, `requirements*.txt`, `environment.yml`, `package.json`, `pnpm-lock.yaml`, `CMakeLists.txt`, `Cargo.toml`, `Makefile`, CUDA files, shell scripts, notebooks, and test commands.
9. **Report repo context**. Stop with blockers when a required repo source remains too ambiguous or cannot be verified against the desired command.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, parent guardrails, and user request, then execute the plan.

## Acquisition Rules

- Use `git clone <source> <topic-workspace-dir>/repos/<repo-name>` for Git sources.
- Copy or link local sources only when the user or gate clearly authorizes that source.
- Do not place task repos in the Project root, Agent Workspace, `.pixi/`, or temporary directories as the durable repo location.
- Do not claim readiness just because a repo exists; repo checks must still be represented in `isomer-env-gate.md` and verified later.

## Output Notes

Carry forward:

- repo name;
- expected path;
- explicit or inferred source;
- source warning, if any;
- relevant files inspected;
- likely dependency signals;
- likely verification commands;
- blockers.
