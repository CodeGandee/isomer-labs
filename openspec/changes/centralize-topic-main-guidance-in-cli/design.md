## Context

The completed `inject-topic-main-agent-guidance` change established that each Topic Main Development Repository should carry root-level `AGENTS.md` and `CLAUDE.md` guidance for external agents. Its first implementation plan placed the full guidance body in service and operator skill reference pages, which creates two problems: the same large string must be maintained in several places, and the code that eventually mutates repository files would still need its own copy.

The repository already has a Click-based `isomer-cli` project command surface, package assets under `src/isomer_labs/assets`, and Jinja2 as a dependency. That makes the CLI a good source of truth for rendering, inspecting, and upserting the guidance block.

## Goals / Non-Goals

**Goals:**

- Store the canonical topic-main guidance body in one packaged `.j2` template asset.
- Render the guidance on demand through `isomer-cli`.
- Inspect and ensure root-level `AGENTS.md` and `CLAUDE.md` through `isomer-cli`.
- Keep large Markdown prose out of Python source.
- Make service and operator skills call the CLI source of truth instead of copying the block body.

**Non-Goals:**

- Do not add topic-specific resolved values to the guidance block.
- Do not make skill docs or tests the authoritative source for the guidance text.
- Do not require a new dependency beyond the existing Jinja2 dependency.
- Do not make the guidance command responsible for creating or repairing `topic.repos.main` itself.
- Do not overwrite content outside the Isomer-managed marked block.

## Decisions

1. Use a packaged `.j2` template asset as the canonical text source.

   Add an asset such as `src/isomer_labs/assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2`. The template owns the body, including the fenced block shape. Python owns only small constants, the template resource path, the render context, and mutation logic.

   Alternative considered: keep the block as a Python multiline string. That would technically centralize the content but would make the large prose harder to read, review, and revise.

2. Add a small domain module for rendering and file operations.

   Add `src/isomer_labs/topic_main_guidance.py` with functions such as:

   - `render_topic_main_guidance_block()`
   - `inspect_topic_main_guidance_file(path)`
   - `upsert_topic_main_guidance_file(path)`
   - `inspect_topic_main_guidance(repo_path)`
   - `ensure_topic_main_guidance(repo_path)`

   The module should load the `.j2` template with `importlib.resources`, render with Jinja2, and use marker-based replacement for idempotent updates.

3. Add a project-scoped CLI group.

   Add:

   ```bash
   isomer-cli project topic-main-guidance render
   isomer-cli --print-json project topic-main-guidance inspect --topic <topic>
   isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes
   ```

   `render` requires no selected topic. `inspect` and `ensure` resolve the selected effective topic context and `topic.repos.main`. `ensure` requires explicit confirmation through `--yes` because it writes `AGENTS.md` and `CLAUDE.md`.

4. Use structured status names for each target file.

   Each target should report statuses such as `missing`, `current`, `stale`, `duplicate`, `malformed`, `unknown_version`, and `unsafe`. Ensure actions should report `created`, `appended`, `updated`, `unchanged`, or `blocked`.

5. Keep the skills thin.

   `isomer-srv-topic-env-setup` should say to run or route to `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` after `topic.repos.main` is safe. `isomer-admin-topic-mgr storage-inspect-main` should say to run `inspect` for read-only posture and `ensure --yes` only for explicit repair. Neither skill should include the full guidance body.

6. Update validators to prevent re-duplication.

   Skillset validation should require references to the CLI commands and the `.j2` template source-of-truth rule. It should reject or flag full copied blocks in service/operator skill docs, especially repeated lines from the canonical body.

## Risks / Trade-offs

- Existing completed change artifacts still mention copied text -> This follow-up should update implementation tasks and skill docs so the applied behavior uses the CLI source of truth.
- CLI `ensure` could be invoked before `topic.repos.main` exists -> The command should resolve `topic.repos.main`, require it to be an existing normal non-bare Git repository, and block with a repair route rather than creating the repository.
- Template rendering could accidentally add topic-specific values -> The default render context should contain placeholders and command forms only. Tests should assert no resolved Research Topic id, path, `manifest_path`, or `pixi_environment` is injected.
- File mutation could corrupt existing rule files -> The upsert logic should replace only content between recognized begin/end markers, append when absent, and block or report diagnostics for duplicate or malformed markers.
- Text and JSON output could drift -> The CLI payload should carry all authoritative status fields, while text output stays concise and human-readable.

## Migration Plan

1. Add the `.j2` asset and rendering module.
2. Add the `project topic-main-guidance` CLI group with `render`, `inspect`, and `ensure`.
3. Update service and operator skills to route through the CLI commands and remove embedded block prose.
4. Update validators to require CLI routing and prevent copied guidance bodies in skill docs.
5. Add unit tests for render output, inspection states, idempotent ensure behavior, JSON payloads, and skill validation.
