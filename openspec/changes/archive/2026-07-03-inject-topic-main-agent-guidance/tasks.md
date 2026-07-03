## 1. Topic Main Guidance Contract

- [x] 1.1 Add the canonical Isomer topic-main guidance block text to the topic env setup documentation, including stable begin/end markers and the `isomer-labs-topic-main-guidance` fenced block.
- [x] 1.2 Ensure the block states that Pixi is the primary package manager and execution environment, Python must run through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...`, and system Python, ambient virtualenvs, plain `python`, plain `pip`, shell activation, and local `.venv` environments are not the source of truth.
- [x] 1.3 Ensure the block directs agents to query topic-specific facts through `isomer-cli` commands and semantic labels instead of embedding resolved topic, actor, agent, runtime, credential, external repository, `manifest_path`, or `pixi_environment` values.

## 2. Topic Env Setup Updates

- [x] 2.1 Update `isomer-srv-topic-env-setup` `ensure-topic-main-repository` instructions to create missing root-level `AGENTS.md` and `CLAUDE.md` in `topic.repos.main` after mutation authorization.
- [x] 2.2 Update the same instructions to preserve existing file content, append the guidance block when absent, and update a recognized stale block in place without duplicating it.
- [x] 2.3 Update setup output requirements to report guidance posture, block version, changed files, blockers, and next action.
- [x] 2.4 Update `setup-topic-env` combined result wording so topic-main readiness includes agent guidance posture.

## 3. Topic Manager Updates

- [x] 3.1 Update `isomer-admin-topic-mgr` storage subcommand listings if a new explicit `storage-refresh-agent-guidance` route is added, or document the explicit repair branch under `storage-inspect-main` if no new public subcommand is needed.
- [x] 3.2 Update `storage-inspect-main` instructions to report whether `AGENTS.md` and `CLAUDE.md` exist and whether each contains the current Isomer-managed guidance block.
- [x] 3.3 Add or update the explicit repair workflow to create missing rule files, append or update the guidance block, preserve unrelated content, block on unsafe repositories, and route canonical repository repair to `isomer-srv-topic-env-setup`.

## 4. Validation

- [x] 4.1 Add or update skillset validation tests to require the guidance markers, fenced block tag, Pixi-primary wording, Python-through-Pixi wording, system-Python avoidance wording, and `isomer-cli` query-first wording.
- [x] 4.2 Run the relevant unit tests for skillset validation.
- [x] 4.3 Run `openspec status --change inject-topic-main-agent-guidance --json` and confirm proposal, design, specs, and tasks remain complete before applying.
