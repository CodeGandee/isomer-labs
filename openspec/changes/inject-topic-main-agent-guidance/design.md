## Context

The Topic Main Development Repository is the shared Git anchor for operator work and prepared actor or agent worktrees. External agents that enter that repository commonly read root-level rule files such as `AGENTS.md` or `CLAUDE.md` before acting, but Isomer currently does not ensure those files explain the local Pixi and `isomer-cli` rules.

Topic environment setup already owns `topic.repos.main` creation and validation. Topic Manager already owns initialized-topic storage inspection and explicit topology repair. The guidance injection should fit those boundaries: initial creation belongs to topic env setup, while later diagnosis and repair belongs to Topic Manager storage commands.

## Goals / Non-Goals

**Goals:**

- Ensure root-level `AGENTS.md` and `CLAUDE.md` exist in topic-main and carry an Isomer-managed fenced guidance block.
- Preserve existing user-authored rule-file content by appending or updating only the Isomer-managed block.
- Make Pixi rules explicit: Pixi is the primary package manager and Python must be invoked through Pixi.
- Keep the guidance topic-independent by directing agents to `isomer-cli` for topic, path, actor, agent, Pixi binding, and runtime facts.
- Let Topic Manager inspect and explicitly repair missing or stale guidance blocks after initialization.

**Non-Goals:**

- Do not encode concrete Research Topic ids, actor names, agent names, absolute topic workspace paths, runtime paths, credentials, external repository paths, or research statements into the guidance block.
- Do not make `AGENTS.md` or `CLAUDE.md` the source of truth for topic context.
- Do not create a new CLI surface for guidance injection unless implementation discovers that the existing skill-level repair route cannot express it.
- Do not overwrite or normalize unrelated user-authored content in existing rule files.

## Decisions

1. Use HTML markers around a fenced block.

   The block should be wrapped with `<!-- BEGIN isomer-labs-topic-main-guidance v1 -->` and `<!-- END isomer-labs-topic-main-guidance v1 -->`, with the body in a fenced code block tagged `isomer-labs-topic-main-guidance`. The markers make updates idempotent, while the fenced block satisfies the requirement that Isomer knowledge be visibly contained.

   Alternative considered: append a plain Markdown section. That is easier to read but harder to update without duplicate prose.

2. Ensure both `AGENTS.md` and `CLAUDE.md`.

   `AGENTS.md` covers AGENTS-aware tools and Codex-style agents. `CLAUDE.md` covers Claude-style agents. The content should be equivalent and tool-neutral, because the important rules are Isomer, Pixi, and `isomer-cli` rules rather than agent-vendor rules.

   Alternative considered: create only the file requested by the active agent. That would miss other actors entering the same topic-main later.

3. Put first-time injection in `ensure-topic-main-repository`.

   This subcommand already creates, reuses, configures, and reports `topic.repos.main`. It has the right mutation confirmation boundary and changed-files output. Adding rule-file posture there makes the guidance part of topic-main readiness.

   Alternative considered: inject during package installation or actor materialization. That would make guidance depend on later steps and could leave the root repo under-documented.

4. Put later inspection and repair in Topic Manager storage commands.

   `storage-inspect-main` should report the presence, freshness, and changed-file posture of the guidance block. An explicit storage repair path, either added to `storage-inspect-main` when the operator asks for repair or exposed as `storage-refresh-agent-guidance`, should update the block without claiming broader environment readiness.

   Alternative considered: route all repairs back to topic env setup. That preserves one owner but makes a small Markdown repair feel heavier than necessary for an initialized topic.

5. Keep the block generic and query-first.

   The block should tell agents to run `isomer-cli --print-json project context show`, `project paths get`, `project paths explain`, `project topics list`, and `project topic-actors list` for details. It should name semantic labels such as `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.records`, `topic.runtime`, `topic.actors.workspace`, and `agent.workspace`, but it should not resolve them inline.

   Alternative considered: embed the currently resolved paths for convenience. That would become stale and would violate the rule that queryable facts come from `isomer-cli`.

## Risks / Trade-offs

- Existing repositories may have strong local conventions for `AGENTS.md` or `CLAUDE.md` -> Preserve all existing content and append only the marked block when absent.
- Agents may treat fenced guidance as inert code rather than instructions -> Surround the fence with stable markers and place the block at the end of the rule file so it is discoverable.
- The block may become stale as CLI commands evolve -> Version the marker with `v1` and make Topic Manager report stale or unknown versions.
- Automatic changes to existing repositories may surprise owners -> Require the same mutation confirmation or service authorization already required for topic-main setup, and report changed files.
- Guidance could accidentally include topic-specific facts -> Keep the block template static and require implementers to verify that generated content contains placeholders or command forms, not resolved topic values.

## Migration Plan

1. Update the topic env setup skill docs so `ensure-topic-main-repository` creates or refreshes `AGENTS.md` and `CLAUDE.md` with the marked fenced block.
2. Update the setup chain output contract so changed files and readiness evidence include guidance file posture.
3. Update Topic Manager storage docs so `storage-inspect-main` reports guidance status and exposes an explicit repair action.
4. Add or update skillset validation tests that inspect the required guidance text, markers, and Pixi/system-Python wording.
5. Existing topic-main repositories can be repaired by rerunning the topic-main setup step with mutation authorization or by using the Topic Manager storage repair route.
