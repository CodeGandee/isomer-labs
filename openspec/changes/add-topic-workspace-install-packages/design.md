## Context

Isomer already has several pieces of package-related policy: service env setup knows Pixi command style and enclosure, research v2 skills know when a task is blocked by missing packages, and the newly proposed tool-pack catalog can describe named toolsets without installing them. The missing piece is a single operator-owned package mutation surface for a Topic Workspace.

The current active research v2 guidance mostly records package availability checks, but some reachable guidance still says to provide `install.packages()` commands, ask permission to install dependencies, or create a local virtual environment. That leaks environment ownership into research skills and creates several possible package mutation paths.

## Goals / Non-Goals

**Goals:**

- Add `install-packages` to `isomer-admin-topic-workspace-mgr` as the public package-add route for a selected Topic Workspace.
- Accept flexible input: plain prompt text, Markdown, YAML, JSON, requirements-style package lists, or copied blocker text.
- Infer package names, package kinds, install commands, verification checks, and blockers from the input without requiring a formal schema-constrained config file.
- Install through the selected Topic Workspace Pixi environment and verify with real import, CLI, runtime, or file-generation checks.
- Make active research v2 skills route missing package or local virtualenv needs to the new operator subcommand.
- Preserve no-sudo, no-system-package-manager, no-ad-hoc-venv, and no-ambient-pip boundaries.

**Non-Goals:**

- Do not create a new package manager or a mandatory request-file schema.
- Do not make research skills install packages directly.
- Do not route automatically to the manual `isomer-misc-tool-packs` skill.
- Do not solve privileged host setup, system package manager mutation, kernel drivers, daemon installs, or machine-global runtime changes.

## Decisions

### Workspace Manager Owns the Public Install Surface

`isomer-admin-topic-workspace-mgr install-packages` should be the command users and skills call when packages need to be added to a Topic Workspace. This makes the operator workspace manager the place that resolves Topic Workspace context, applies workspace mutation policy, installs, verifies, and reports evidence.

Alternative considered: keep using `isomer-srv-topic-env-setup install-topic-deps` as the public package-add route. That keeps package work near environment setup, but it leaves research skills deciding when to enter service setup and does not provide the simple operator command users asked for.

### Flexible Intake, Structured Internal Plan

The subcommand should accept unstructured and structured input. If the user gives plain text such as "install matplotlib scipy for Python figures", the skill infers package names and checks. If the user gives Markdown, YAML, JSON, or a requirements-style list, the skill extracts the same information from that source. Internally it should normalize to an install plan, but that plan is an implementation artifact, not a required user-facing schema.

Alternative considered: require a strict package request file. That would make validation easier, but it would be too heavy for interactive operator use and copied research blockers.

### Install and Verify in the Topic Workspace Pixi Environment

The install plan should resolve the selected Topic Workspace and Pixi binding before mutation. Python libraries should be installed into the selected Topic Workspace Pixi environment, native or Conda-style tools should use Pixi/Conda channels as appropriate, R packages should be installed through a workspace-controlled route, and verification should run through Pixi-scoped commands.

Alternative considered: allow the research skill to suggest `pip`, `install.packages()`, or a local virtual environment. That is convenient locally, but it fractures reproducibility and bypasses Topic Workspace ownership.

### Research Skills Become Requesters, Not Installers

Active research v2 skills should report missing package or runtime blockers and route package additions to `$isomer-admin-topic-workspace-mgr install-packages`. They can include package names, purpose, backend, and desired verification checks in natural language, but they should not provide direct install commands or local virtualenv recipes.

Alternative considered: let each research skill keep domain-specific install snippets. That would preserve source skill behavior, but it repeats package policy and makes future environment routing inconsistent.

### Service Setup Becomes Non-Bypassing

Service env setup can still hold useful Pixi and enclosure policy, but user-facing or cross-skill package-add requests should not bypass the workspace manager. If service guidance remains relevant during implementation, it should be used through or under the operator-owned route rather than as a competing entrypoint.

Alternative considered: keep two equivalent entrypoints. That would be easier to implement incrementally, but it would violate the "all package installation routes through workspace manager" rule and keep ambiguity alive.

## Risks / Trade-offs

- Ambiguous package descriptions -> Ask a targeted clarification or report a blocker before mutation.
- Wrong package source inference -> Record why the chosen route was selected and verify the actual import, executable, or runtime behavior.
- R package installation details vary by Pixi/R setup -> Keep R installation workspace-scoped and block when the selected Topic Workspace cannot support a safe R route.
- Large native dependencies can be expensive -> Reuse bounded-run/resource guidance before heavy installs or verification commands.
- Existing service setup wording may conflict -> Update service guidance enough that direct package-add requests route to the workspace manager.

## Migration Plan

1. Add `install-packages` to the workspace manager entrypoint, help, subcommand table, output contract, and guardrails.
2. Add `references/install-packages.md` with flexible intake, inference, install planning, Pixi mutation, verification, blocker, and reporting guidance.
3. Update active research v2 guidance that currently provides direct package install or local virtualenv instructions to route package needs to the workspace manager.
4. Update service setup guidance so package-add requests from users or other skills do not bypass the workspace manager route.
5. Validate operator, service, and research skillsets, then run OpenSpec strict validation.

Rollback is straightforward: remove the new subcommand page and entrypoint references, then restore research/service guidance to the previous package handling language. No persisted runtime migration is required.

## Open Questions

- Should R packages be installed through Pixi-provided R plus an in-workspace R library path, through Conda packages when available, or selected per request?
- Should CLI tools requested as reusable user tools ever use `uv tool install` or `pixi global install` from this operator route, or should this subcommand keep all installs inside the Topic Workspace Pixi environment by default?
