## Context

The current implementation has the semantic path model, Topic Workspace Manifest default profile, Topic Main Repository term, `isomer-managed/` worker namespace, docs validation for tmp wording, and topic-env literal `tmp/` ignore posture. The canonical domain language already defines **Local Tmp Surface** and names `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.

What is still missing is the executable contract: the semantic surface catalog does not yet expose those labels, the path resolver cannot return them, runtime validation does not know which paths are disposable tmp paths, and the operator/service skills do not yet validate `topic.main_repo.tmp` and `agent.tmp` ignore posture as first-class evidence.

The important semantic distinction remains `tmp/` versus `isomer-managed/agent-owned/scratch/`. `scratch/` is an agent-owned support surface for local drafts that might later be promoted. `tmp/` is lower value: it is sweepable, ignored, and forbidden as a dependency for runtime records, evidence, handoffs, Provenance Records, Peer Read Access, or profile readiness.

## Goals / Non-Goals

**Goals:**

- Promote `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` from planned documentation posture to implemented semantic workspace surfaces.
- Under `isomer-default.v1`, bind those labels to `<topic-workspace>/tmp/`, `<resolved topic.main_repo>/tmp/`, and `<resolved agent.workspace>/tmp/`.
- Classify every tmp surface as local, ignored, disposable, non-shared, and not durable evidence.
- Ensure setup flows that own a root prepare or validate the nearest ignore policy: Topic Workspace root `.gitignore` for `topic.tmp`, and Topic Main Repository root `.gitignore` for `topic.main_repo.tmp` and Git-worktree `agent.tmp`.
- Extend validation, operator skills, service setup guidance, and documentation so each tmp surface has consistent label naming, path-source evidence, and diagnostics.
- Report durable references to tmp material as invalid dependencies that need promotion before the referring record can be treated as ready.

**Non-Goals:**

- Do not make `tmp/` a sharing mechanism.
- Do not record tmp contents as durable runtime state, durable readiness evidence, or approved profile material.
- Do not replace `isomer-managed/agent-owned/scratch/`, `public/`, `topic-owned/`, owner-preserved `records/*`, or Git-tracked collaboration files.
- Do not delete, archive, move, or promote existing `tmp/` contents automatically during validation.
- Do not add `.gitkeep` files or tracked sentinel files under ignored tmp directories.

## Current Baseline Decisions

### Decision: Keep the existing docs-validation posture as a guard

Current docs validation already rejects `tmp/` wording that fails to mention semantic labels, disposable semantics, and not-durable semantics. This change keeps that guard and updates user docs from "planned/downstream" wording to implemented first-class label wording.

### Decision: Preserve topic-env literal tmp ignore behavior

`isomer-srv-topic-env-setup` already writes `tmp/` into the Topic Workspace `.gitignore` during dependency setup. This change does not remove that behavior. After `topic.tmp` exists as a resolver label, the service should report the label and path source when available, while continuing to support the default `tmp/` ignore posture.

## Design Decisions

### Decision: Add tmp labels to the semantic surface catalog

The standard disposable surfaces are:

- `topic.tmp`: topic-scoped disposable local material, default `tmp/`.
- `topic.main_repo.tmp`: owner-checkout disposable material inside the resolved Topic Main Repository, default `repos/topic-main/tmp/`.
- `agent.tmp`: per-agent disposable material inside the resolved Agent Workspace, default `agents/{agent_name}/tmp/`.

Each surface should use a disposable durability classification and a non-shared/private sharing classification. Compatibility ids should be explicit, such as `topic_tmp`, `topic_main_tmp`, and `agent_tmp`, so CLI/API output can remain stable without callers assembling paths by string.

Alternative considered: leave tmp surfaces as prose-only labels. That would preserve current docs but leave services and validators unable to reason about resolved paths, custom bindings, or durable dependency violations.

### Decision: Ignore tmp through the nearest relevant Git policy

The Topic Workspace root `.gitignore` owns the default `topic.tmp` binding. The resolved Topic Main Repository root `.gitignore` owns default `topic.main_repo.tmp` and `agent.tmp` bindings when Agent Workspaces are Git worktrees of that repository.

Alternative considered: add ignore rules only under `isomer-managed/`. That would not cover root `tmp/` in the Topic Main Repository or Agent Workspace cwd, which is exactly where generic tools tend to create disposable files.

### Decision: Do not treat tmp labels as durable runtime truth

Path preview and explicit materialization may report or create tmp labels. Runtime records, handoffs, Artifact locators, Evidence Items, Decision Records, Provenance Records, readiness outputs, and profile material must not depend on tmp paths. If a diagnostic or path-plan surface has to mention a tmp path, it must mark the path as disposable posture, not durable evidence.

Alternative considered: persist tmp path plans alongside durable runtime path plans. That would make disposable state look authoritative and invite later code to depend on it.

### Decision: Missing directory severity differs from missing ignore policy

Setup and explicit materialization may create missing tmp directories. Read-only validation should warn when an expected resolved tmp directory is absent, but missing or ineffective ignore policy, tracked tmp contents, and durable references to tmp material should block readiness for the workflow that depends on that posture.

Alternative considered: make every missing tmp directory an error. That is too strict for existing workspaces because tmp is disposable and may be absent until a tool needs it.

### Decision: Do not add `.gitkeep`

Ignored tmp directories should remain empty and untracked unless a local tool creates disposable content. The system should not add `.gitkeep`, placeholder files, or tracked markers under tmp labels.

Alternative considered: add `.gitkeep` to force directory existence in Git. That conflicts with the disposable and ignored contract.

## Risks / Trade-offs

- Existing workflows may already use ad hoc temporary files under durable roots. Mitigation: validation should point users toward `tmp/` and explain promotion routes without deleting files.
- A user may put important work under `tmp/` anyway. Mitigation: validation should explain that such material must be promoted to `records/*`, Git-tracked material, or an approved sharing surface before another record depends on it.
- Multiple ignore policies can feel redundant. Mitigation: keep the rule simple: each root that can be a Git root or command root gets a local `tmp/`, and the nearest `.gitignore` ignores it.

## Migration Plan

1. Update delta specs and docs to reflect that semantic path resolution and Local Tmp Surface language already exist in the baseline.
2. Add the tmp labels to the semantic surface catalog and default profile.
3. Update path resolution, CLI output, and tests for `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
4. Update setup/materialization flows to prepare missing tmp directories and ignore policies when they own the relevant root.
5. Update validation to report durable references to tmp, tracked tmp contents, and missing or ineffective ignore policies without deleting existing files.
6. Update operator and service skills to prepare and validate the tmp contract.

Rollback is low risk before implementation because the artifacts only define expected behavior. After implementation, rollback means removing creation and diagnostics for the new tmp surfaces while leaving existing ignored directories untouched.
