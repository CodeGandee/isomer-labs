## 1. Template Asset and Renderer

- [x] 1.1 Add `src/isomer_labs/assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2` as the only canonical large-text source for the topic-main guidance body.
- [x] 1.2 Add a topic-main guidance module that loads the `.j2` asset with `importlib.resources`, renders it through Jinja2, and supplies only small constants plus a dynamic render context from Python.
- [x] 1.3 Ensure rendered guidance includes the current begin marker, end marker, `isomer-labs-topic-main-guidance` fenced block tag, Pixi-primary wording, Python-through-Pixi command form, CLI query forms, and semantic-label placeholders without resolved topic-specific values.

## 2. Guidance Inspection and Upsert Logic

- [x] 2.1 Implement file inspection for root `AGENTS.md` and `CLAUDE.md` statuses: `missing`, `current`, `stale`, `duplicate`, `malformed`, `unknown_version`, and `unsafe`.
- [x] 2.2 Implement idempotent upsert behavior that creates missing files, appends when absent, updates recognized stale blocks in place, preserves all content outside the marked block, and blocks on duplicate or malformed markers.
- [x] 2.3 Implement repository-level inspection and ensure functions that operate only on an existing safe normal non-bare `topic.repos.main` and report changed files, target statuses, blockers, and guidance metadata.

## 3. CLI Commands

- [x] 3.1 Add `project topic-main-guidance render`, `inspect`, and `ensure` to the Click command surface and root help command list.
- [x] 3.2 Implement `render` so it does not require Project or Topic context and emits the rendered guidance in text or JSON form.
- [x] 3.3 Implement `inspect` so it resolves effective Topic context and `topic.repos.main`, checks both guidance files without mutation, and emits deterministic text and JSON output.
- [x] 3.4 Implement `ensure --yes` so it requires explicit confirmation, resolves `topic.repos.main`, performs idempotent upsert only on safe repositories, and emits deterministic text and JSON output.

## 4. Skill and Validator Rewiring

- [x] 4.1 Update `isomer-srv-topic-env-setup` guidance instructions so `ensure-topic-main-repository` routes rendering and mutation through `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or an equivalent CLI-backed API.
- [x] 4.2 Update `isomer-admin-topic-mgr` `storage-inspect-main` so inspection routes through `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` and explicit repair routes through `ensure --yes`.
- [x] 4.3 Remove copied full guidance body prose from service and operator skill docs while retaining concise policy summaries and command examples.
- [x] 4.4 Update `scripts/validate_skillsets.py` and fixture tests so skills must reference the CLI source of truth and `.j2` template contract, and copied full guidance blocks are rejected or diagnosed.

## 5. Tests and Verification

- [x] 5.1 Add CLI unit tests for render output, JSON payload metadata, topic-independent rendering, inspect statuses, ensure mutation, and idempotent second ensure.
- [x] 5.2 Add CLI unit tests that confirm `ensure` without `--yes` and unsafe `topic.repos.main` states block without mutation.
- [x] 5.3 Run focused CLI and skillset validation tests.
- [x] 5.4 Run `python scripts/validate_skillsets.py`.
- [x] 5.5 Run `pixi run test`.
- [x] 5.6 Run `openspec instructions apply --change centralize-topic-main-guidance-in-cli --json` and confirm all tasks are complete.
