## Context

The active operator surface now consists of focused owner skills: `isomer-admin-project-mgr`, `isomer-admin-topic-creator`, `isomer-admin-topic-mgr`, `isomer-admin-topic-team-specialize`, and `isomer-admin-houmao-interop`. These skills have clear boundaries, but a new user still needs to know which path to choose before invoking the correct owner skill.

The welcome skill is not a replacement for those owners. Its job is to say what Isomer Labs can do, list the available paths, name the skill to invoke for each path, and optionally recommend one path from the user's prompt or read-only Project context.

The design must also respect recent operator-surface cleanup. `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, and `isomer-admin-manual-research-session` are retired and must not appear as active routes. Operator skills also must not own research-paradigm v2 bootstrap, which belongs to `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2` or later research-stage skills.

## Goals / Non-Goals

**Goals:**

- Add `isomer-admin-welcome` as a user-facing capability menu and path chooser.
- Make the default interaction action-oriented: list supported workflows, name direct owner-skill invocations, and invite the user to choose a path or describe their goal.
- Provide an optional `next-step` mode that can inspect current context with read-only commands and recommend a safe owner workflow.
- Keep the welcome skill small, local-reference based, and consistent with command-style operator skill conventions.
- Validate naming, metadata, local references, read-only default posture, owner-skill routing, and retired-skill exclusions.

**Non-Goals:**

- Do not teach the full Isomer system model as the primary experience.
- Do not duplicate owner skill workflows or subcommand details beyond enough text to choose a path.
- Do not initialize Projects, create Research Topics, mutate Topic Workspaces, install packages, specialize teams, launch agents, or bootstrap research-paradigm v2 artifacts.
- Do not add automatic routing to the manual `isomer-misc-tool-packs` skill.

## Decisions

1. Make `show-options` the default mode.

   The welcome skill should behave like a menu, not a tutorial. An empty invocation or broad request such as "what can Isomer Labs do?" should print supported options with owner skills and direct invocation guidance.

   Alternative considered: default to a conceptual introduction. That makes the skill verbose and does not solve the user's immediate routing problem.

2. Keep subcommands narrow.

   The skill should expose `help`, `show-options`, `choose-path`, `show-skill-map`, and `next-step`. `choose-path` interprets the user's goal without mutating state. `show-skill-map` is a compact direct-invocation table. `next-step` can use read-only context checks when a Project is available.

   Alternative considered: include `explain-concepts` as a public route. That can become a second documentation system, so concept explanations should remain brief supporting text inside options or help.

3. Route only to active owner skills.

   The supported path list should cover Project setup and checks, topic creation and manual-research-ready preparation, initialized-topic management, Topic Team Specialization, and Houmao interop. It may mention service skills only as delegated lower-level owners, not as ordinary first-click user paths.

   Alternative considered: expose every service and research skill in the welcome menu. That would overwhelm new users and blur operator versus service versus research-stage boundaries.

4. Make read-only context inspection optional and explicit.

   `next-step` may run commands such as `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project topics list`, and `isomer-cli project context show`. It must report that it is inspecting context and must not run mutating commands.

   Alternative considered: always inspect context before printing the menu. That slows the default path and can surprise users who only wanted the option list.

5. Treat tool packs as manual invocation only.

   The welcome skill can omit `isomer-misc-tool-packs` from the primary operator menu or mention it only as a manual skill when the user explicitly asks for installable toolsets. It must not auto-route tool-pack installation.

   Alternative considered: include tool packs as a main welcome path. That would encourage environment mutation from the welcome surface and conflict with the current manual-invocation design.

## Risks / Trade-offs

- [Risk] The welcome skill becomes another long documentation page. → Mitigation: require action-oriented options, owner skill names, and direct invocation text as the default output.
- [Risk] The skill accidentally revives retired routes. → Mitigation: validation should scan welcome guidance for retired skill names as active invocations.
- [Risk] The menu hides service skills that advanced operators need. → Mitigation: describe service skills as delegated owners inside relevant paths, while keeping primary paths user-facing.
- [Risk] Context-aware recommendation could look like mutation. → Mitigation: restrict `next-step` to read-only commands and report commands run in Complete Output.
- [Risk] The manifest currently contains retired compatibility skill entries. → Mitigation: include cleanup in implementation tasks so the core manifest matches active operator inventory before validation passes.
