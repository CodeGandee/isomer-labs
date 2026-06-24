## Context

Isomer currently treats the Project root as the Houmao project directory during Project initialization. The call shape is effectively `houmao-mgr --print-json project --project-dir <project-root> init`, so Houmao creates `<project-root>/.houmao/`. That root-level overlay can collide with a user's existing Houmao project in the same repository or workspace.

The repository already has an Isomer-owned Project Config Directory at `<project-root>/.isomer-labs/`. Houmao's CLI supports redirecting the Houmao project directory with `--project-dir`, so Isomer can make `<project-root>/.isomer-labs/` the Houmao project directory and let Houmao create `<project-root>/.isomer-labs/.houmao/`.

Current code also uses `houmao_project_dir` inconsistently. In some places it means the Houmao CLI `--project-dir` value, while in init and output it effectively means the `.houmao/` overlay path. The implementation should separate these concepts:

- **Isomer Project root**: `<project-root>/`
- **Project Config Directory**: `<project-root>/.isomer-labs/`
- **Isomer-managed Houmao project directory**: `<project-root>/.isomer-labs/`, the value passed to Houmao `--project-dir`
- **Isomer-managed Houmao overlay**: `<project-root>/.isomer-labs/.houmao/`, the state directory Houmao creates under the redirected project directory
- **Root Houmao overlay**: `<project-root>/.houmao/`, external/user-owned if present

## Goals / Non-Goals

**Goals:**

- Prevent Isomer from mixing its Houmao bootstrap state with user-owned root `.houmao/`.
- Use Houmao's existing `--project-dir` redirect support instead of adding a new storage mechanism.
- Keep Project initialization, cleanup, path safety, manifests, CLI output, tests, and project-manager skill guidance consistent about `.isomer-labs/.houmao/`.
- Preserve existing side-effect boundaries: init may bootstrap static Project-level Houmao state, while runtime launch, stop, messaging, inspection, and adoption remain separate commands.
- Make cleanup preserve root `.houmao/` even when cleanup targets the Isomer-managed Houmao overlay.

**Non-Goals:**

- Do not migrate, delete, inspect, or adopt an existing root `.houmao/` directory.
- Do not make the Isomer-managed Houmao project directory user-configurable in the Project Manifest.
- Do not change per-Agent Team Instance adapter material paths under Topic Workspaces.
- Do not repair live Houmao managed agents, installed runtimes, Pixi environments, or external Houmao state that may depend on old paths.

## Decisions

### Use `.isomer-labs/` as Houmao `--project-dir`

Project init should call Houmao with `<project-root>/.isomer-labs/` as the redirected project directory. Houmao then owns `<project-root>/.isomer-labs/.houmao/` internally.

Alternative considered: pass `<project-root>/.isomer-labs/.houmao/` as `--project-dir`. That would likely make Houmao create `<project-root>/.isomer-labs/.houmao/.houmao/`, which does not match the requested layout and makes the command contract harder to explain.

Alternative considered: keep using root `<project-root>/.houmao/` and add collision detection. That still mixes Isomer and user Houmao state when a root overlay exists, so it does not solve the ownership problem.

### Derive the internal Houmao path instead of storing it in the manifest

The Isomer-managed Houmao project directory should be derived as `config_dir_for_root(project_root)`. The overlay should be derived as `config_dir_for_root(project_root) / ".houmao"`.

Alternative considered: add a Project Manifest path setting. That adds configuration surface and creates new unsafe states, such as pointing Isomer back at root `.houmao/`. The location is an implementation detail owned by Isomer, so a fixed derived path is simpler and safer.

### Report both project directory and overlay deliberately

Implementation should avoid using one ambiguous field for both concepts. CLI JSON may retain `houmao_project_dir` for compatibility only if it means the Houmao `--project-dir` value. New or revised output should expose `houmao_overlay_dir` for the actual `.houmao/` path. Human-readable output should say `Houmao Project Directory` for `.isomer-labs/` and `Houmao Overlay` for `.isomer-labs/.houmao/`.

Alternative considered: keep `houmao_project_dir` as the overlay path. That preserves old output shape but conflicts with Houmao's own `--project-dir` wording and risks future bugs.

### Treat root `.houmao/` as external state

Project init should not fail merely because `<project-root>/.houmao/` exists. It may emit a warning that the root overlay is external and ignored by Isomer. Cleanup should never plan root `.houmao/` for removal.

Alternative considered: fail init when root `.houmao/` exists. That avoids ambiguity but blocks valid users who already use Houmao in the same repository, which is the case this change is meant to support.

### Keep content roots away from Isomer config and known Houmao state

Generated content roots must still be Project-local and must not live under `.isomer-labs/`. Because `.isomer-labs/.houmao/` is inside `.isomer-labs/`, existing Project Config Directory checks already protect the new overlay. Root `.houmao/` should still be rejected as a generated content root because it is a known external Houmao state location, but diagnostics should describe it as external/user-owned rather than Isomer-managed.

## Risks / Trade-offs

- [Risk] Existing tests and code may assume `houmao_project_dir` equals `<project-root>/.houmao/`. → Mitigation: update tests and output assertions to distinguish the redirected Houmao project directory from the overlay directory.
- [Risk] Existing Projects may already contain Isomer-created root `.houmao/`. → Mitigation: new cleanup does not delete it automatically; users can handle that external directory manually after review.
- [Risk] Project cleanup with `--part bootstrap` could double-plan `.isomer-labs/` and `.isomer-labs/.houmao/`. → Mitigation: dedupe or mark the overlay as covered by Project Config cleanup when both parts are selected.
- [Risk] Adapter manifests written before this change may point to root `.houmao/`. → Mitigation: treat old manifests as historical records; new material writes the derived internal project directory.
- [Risk] Operators may still use old skill text that names root `.houmao/`. → Mitigation: update the `isomer-admin-project-mgr` skill entrypoint and local references in the same change.

## Migration Plan

1. Add small helpers or local constants for the Isomer-managed Houmao project directory and overlay path.
2. Update Project initialization to create `.isomer-labs/`, call Houmao with `.isomer-labs/` as `--project-dir`, verify `.isomer-labs/.houmao/`, and report the internal paths.
3. Update cleanup planning so `houmao-overlay` targets `.isomer-labs/.houmao/` and root `.houmao/` is skipped as external state.
4. Update path-safety diagnostics, adapter link manifest defaults, and read-only Houmao status calls to use the derived internal Houmao project directory.
5. Update operator skill guidance and OpenSpec delta requirements.
6. Update unit tests and run lint, typecheck, and unit tests.

Rollback is straightforward for code but not for state: reverting the code would make new Projects use root `.houmao/` again. No automatic file migration should run in either direction.

## Open Questions

None. The design fixes the Isomer-managed Houmao overlay under `.isomer-labs/` and treats root `.houmao/` as external/user-owned state.
