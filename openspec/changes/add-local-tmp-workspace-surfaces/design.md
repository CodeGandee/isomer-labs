## Context

The current workspace layout has durable roots, Git-shared roots, agent-owned support roots, and topic-owned projection roots, but it does not define a simple local tmp convention for disposable files at every place an operator or worker naturally runs commands. The manifest-backed semantic path model means this convention should be expressed through labels, not through an implied directory contract.

This change depends on `add-topic-workspace-manifest-path-resolution`. The default layout may bind `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` to root-level `tmp/` directories, but callers must discover those paths through Workspace Path Resolution.

The important semantic distinction is between `tmp/` and `isomer-managed/agent-owned/scratch/`. `scratch/` is an agent-owned support surface for local drafts that might later be promoted. `tmp/` is lower value: it is sweepable, ignored, and forbidden as a dependency for runtime records, evidence, handoffs, or Peer Read Access.

## Goals / Non-Goals

**Goals:**

- Define `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as standard local disposable surfaces.
- Under `isomer-default.v1`, bind those labels to `<topic-workspace>/tmp/`, `<resolved topic.main_repo>/tmp/`, and `<resolved agent.workspace>/tmp/`.
- Ensure the Topic Workspace root ignore policy covers `topic.tmp` and the resolved Topic Main Repository root ignore policy covers `topic.main_repo.tmp` and Git-backed `agent.tmp`.
- Extend path resolution, runtime setup, validation, operator skills, service setup guidance, and documentation so each surface has consistent label naming, path-source evidence, and diagnostics.
- Make validation report references to `tmp/` from durable runtime records, handoffs, provenance, evidence, or sharing surfaces as invalid dependencies.

**Non-Goals:**

- Do not make `tmp/` a sharing mechanism.
- Do not record `tmp/` paths as durable path plans for downstream research state.
- Do not replace `isomer-managed/agent-owned/scratch/`, `public/`, `topic-owned/`, owner-preserved `records/*`, or Git-tracked collaboration files.
- Do not delete existing `tmp/` contents automatically during validation.

## Decisions

### Decision: Use semantic tmp labels with root-level default bindings

The standard disposable surfaces are `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`. Under `isomer-default.v1`, they resolve to root-level `tmp/` directories at the Topic Workspace root, resolved Topic Main Repository root, and resolved Agent Workspace root. This keeps the user-facing API semantic while preserving convenient command-root defaults.

Alternative considered: place every temporary file under `isomer-managed/agent-owned/scratch/tmp/`. That would hide generic tool scratch inside an Isomer-owned support path and blur the difference between local drafts and disposable files.

### Decision: Ignore `tmp/` through nearest Git policy

The Topic Workspace root `.gitignore` owns the default `topic.tmp` binding. The resolved Topic Main Repository root `.gitignore` owns default `topic.main_repo.tmp` and `agent.tmp` bindings when Agent Workspaces are Git worktrees of that repository.

Alternative considered: add ignore rules only to `isomer-managed/.gitignore`. That would not cover root `tmp/` in the Topic Main Repository or Agent Workspace cwd, which is exactly where generic tools tend to create disposable files.

### Decision: Treat `tmp/` as non-durable even when path preview names it

Path resolution should resolve `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` labels so operators and launch contexts can display expected locations. Runtime records should not depend on tmp paths as durable evidence or handoff inputs. Validation should report tmp references from durable runtime dependencies as errors or blockers.

Alternative considered: record `tmp/` path plans alongside durable runtime directories. That would make disposable state look authoritative and invite later code to depend on it.

## Risks / Trade-offs

- Existing workflows may already use ad hoc temporary files under durable roots → Mitigation: document migration to `tmp/` and add diagnostics for durable references to `tmp/` without deleting files.
- A user may put important work under `tmp/` anyway → Mitigation: validation should explain that such material must be promoted to `records/*`, Git-tracked material, or an approved sharing surface before another record depends on it.
- Multiple ignore policies can feel redundant → Mitigation: keep the rule simple: each root that can be a Git root or command root gets a local `tmp/`, and the nearest `.gitignore` ignores it.

## Migration Plan

1. Update docs and domain language to define tmp labels as local disposable material.
2. Add Workspace Path Resolution support for `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
3. Update runtime initialization and Agent Team Instance workspace preparation to create resolved tmp directories and expected ignore policies when they own the relevant root.
4. Update validation to report missing ignore policy and durable references to `tmp/`, without deleting existing files.
5. Update operator and service skills to prepare and validate the `tmp/` contract.

Rollback is low risk before implementation because the artifacts only define expected behavior. After implementation, rollback means removing creation and diagnostics for the new `tmp/` surfaces while leaving existing ignored directories untouched.

## Open Questions

- Should validation severity for missing resolved tmp directories be `warning` while missing ignore policy is `error`, or should both start as warnings for compatibility?
- Should runtime setup create empty `.gitkeep` files under ignored tmp directories, or should it leave them empty and untracked?
