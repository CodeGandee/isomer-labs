## Why

Isomer currently rejects `project init` when the selected target sits inside an existing Isomer Project, but the intended model is Git-like: nested Projects are allowed, and cwd-based discovery binds to the nearest Project Manifest. This matters for temporary experiments, generated test Projects, and research sandboxes such as `tmp/test-projects/fa4-whitebox-model`.

## What Changes

- Allow `isomer-cli project init` to create a new Project root inside an existing Isomer Project tree.
- Keep discovery nearest-first: a command run inside a nested Project resolves the nested Project, while a command run in the parent outside the nested Project resolves the parent.
- Preserve explicit selector precedence: `--root` and `--manifest` continue to override cwd discovery.
- Remove the current nested-Project initialization rejection and its `ancestor_project_root` failure payload.
- Add regression tests for nested initialization and nearest nested discovery.
- Audit cleanup and content-root authority behavior so parent-scoped operations do not accidentally treat nested Project state as the active Project unless explicitly selected.

## Capabilities

### New Capabilities

### Modified Capabilities
- `isomer-cli-project-discovery`: Project initialization and discovery requirements change to allow nested Project roots and require nearest-Project resolution.

## Impact

- Affected CLI handler: `src/isomer_labs/cli/handlers/project.py`.
- Affected discovery contract: `src/isomer_labs/project/__init__.py` nearest ancestor lookup remains canonical.
- Affected tests: CLI unit tests for Project init/discovery.
- Affected documentation/specs: Project discovery OpenSpec and CLI manual wording that implies nested Projects are rejected.
- No new dependencies or public command names.
