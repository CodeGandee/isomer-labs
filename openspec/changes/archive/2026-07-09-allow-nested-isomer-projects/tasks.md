## 1. Project Init Behavior

- [x] 1.1 Remove the ancestor Project rejection from `project init` while preserving topic-argument rejection and selected-root overwrite refusal.
- [x] 1.2 Ensure nested initialization reports the nested Project root and does not mutate the ancestor Project Manifest.

## 2. Discovery Semantics

- [x] 2.1 Confirm cwd-based discovery keeps nearest ancestor manifest semantics.
- [x] 2.2 Confirm explicit `--root` and `--manifest` selectors still override nearest cwd discovery.

## 3. Tests and Docs

- [x] 3.1 Replace the nested-init rejection unit test with a nested-init success test.
- [x] 3.2 Add or update unit tests proving commands inside a nested Project resolve the child Project and commands outside the child resolve the parent Project.
- [x] 3.3 Update active specs and user-facing docs that state nested Project init is rejected.
- [x] 3.4 Run `openspec validate allow-nested-isomer-projects --strict`, targeted CLI tests, `pixi run lint`, and `pixi run typecheck`.
