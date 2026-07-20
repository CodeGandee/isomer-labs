# Inspect Effective State

## Workflow

1. **Resolve inspection target**: Toolbox registration, callback records, Runtime Param values, imports, gating, source path, or diagnostics.
2. **Resolve scope selectors**. Use Project, Research Topic, Topic Actor, or Topic Agent selectors; use `--topic-agent` for Topic Agent selection.
3. **Use read-only CLI commands** such as `project toolboxes list/show/explain/validate`, `project skill-callbacks list/show/resolve/validate`, and `project toolbox-params get/explain/validate`.
4. **Explain effective state** by distinguishing authored source, installed registration, callback registry rows, Runtime Param import defaults, explicit Runtime Param rows, and Toolbox status gates.
5. **Report Essential Output** with status, scope, ids, source refs, effective values, gating result, diagnostics, blockers, and next action.

If the inspection request does not map cleanly to these steps, use your native planning tool to run the smallest read-only command set and explain what remains unknown.

## Inspection Rules

- Inspection must not mutate Toolbox source, callback registries, Project Manifests, Topic Workspace Manifests, or import files.
- Missing optional registries can be diagnostics rather than blockers.
- Disabled Toolbox status can gate callback resolution without deleting callback records.

