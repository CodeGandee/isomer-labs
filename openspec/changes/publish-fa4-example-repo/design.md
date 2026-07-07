## Context

The FlashAttention-4 white-box runtime-model topic workspace (`flash-attention-4-whitebox-runtime-model`) contains a complete research artifact chain: the analytical predictor source, calibration/validation harness, NCU evidence, paper drafts, and operator-actor worktrees. The goal is to publish a sanitized, reproducible copy of this workspace as a public example repository under the `CodeGandee` GitHub organization.

The source workspace currently contains:
- A 5.6 GB `.pixi/` environment that can be recreated from `pixi.toml` + `pixi.lock`.
- Vendored upstream repositories (`flash-attention`, `accel-sim-framework`) and simulator checkouts in `tmp/`.
- Host-specific identifiers (`huangzhe`, `b200-14-hz`, `/data/ssd1/huangzhe/...`).
- Encrypted chatlog archives and layout-check image artifacts.
- A single Git repository (`repos/topic-main`) with one actor worktree (`actors/operator`).

## Goals / Non-Goals

**Goals:**
- Create `CodeGandee/isomer-example-fa4-analytical-model` as a clean public repository.
- Remove or replace any content that is redownloadable, regenerable, or host-specific.
- Preserve the main-repo + actor-worktree topology by mapping worktrees to branches and attaching them as submodules.
- Provide clear setup instructions so a fresh user can reproduce the environment and build the paper.

**Non-Goals:**
- Do not modify the source Isomer Labs project code or the original topic workspace.
- Do not publish raw encrypted chatlogs or private conversation history.
- Do not attempt to rewrite Git history in the original repository; the public repo will be a fresh sanitized export.

## Decisions

### 1. Single public repo with branch-per-actor submodules

**Decision:** Map the topic main worktree to the public `main` branch and the operator actor worktree to a public `actor-operator` branch. In `main`, register `actors/operator` as a submodule whose URL is the same repo and whose tracked branch is `actor-operator`.

**Rationale:** This satisfies the requirement that actor worktrees “become branches of the new repo” while keeping repository count low. Users can clone with `--recurse-submodules` and get the full topology. The alternative—creating a separate repo per actor—adds management overhead and duplicates object storage.

**Alternative considered:** Flatten actor content into regular directories in `main`. Rejected because it loses the worktree/branch topology that documents the Isomer workflow.

### 2. Exclude `.pixi/`, `tmp/`, and caches

**Decision:** Keep `pixi.toml` and `pixi.lock` in the repo; exclude `.pixi/`, `tmp/`, `.mypy_cache/`, `page_images/`, and layout-check PNGs. Provide `scripts/setup-extern.sh` to re-clone external simulators with `--depth=1`.

**Rationale:** The Pixi lockfile fully determines the environment, so `.pixi/` is unnecessary. Simulator checkouts are redownloadable. Caches and verification images are regenerable.

### 3. Convert vendored upstream repos to proper submodules

**Decision:** Replace `repos/extern/flash-attention/` and `repos/extern/accel-sim-framework/` with Git submodules pointing to their upstream repositories at the commits used in this workspace.

**Rationale:** These are third-party dependencies. Including their full history bloats the example repo and makes updates hard. Submodules keep the dependency link explicit and lightweight.

### 4. Sanitize via export-time rewriting, not in-place editing

**Decision:** Build a sanitization script that operates on a fresh export of the workspace content, replacing host identifiers before the initial commit to the public repo.

**Rationale:** Rewriting history of the original repo is risky and unnecessary. A clean export also lets us choose exactly what goes public and omit private artifacts.

### 5. Keep sanitized records and intent, drop raw chatlogs

**Decision:** Publish sanitized versions of `records/` and `intent/` (with host identifiers masked). Replace `chatlogs/raw/` with a short `chatlogs/README.md` describing the research narrative.

**Rationale:** Records and intent contain valuable reproducibility context. Raw chatlogs are large, encrypted, and contain conversational detail not needed for reproduction.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Self-referencing submodule confuses GitHub UI or recursive clones | Document the layout in `README.md`; use `git submodule update --remote` for actor updates. |
| Sanitization misses a host identifier | Use a two-step scan: literal replacements first, then regex for path patterns; review diff before push. |
| Submodule commit in `main` becomes stale when `actor-operator` advances | Add a CI check or manual step to run `git submodule update --remote` and commit the pointer update. |
| Published repo is still large if figures are kept in full fidelity | Keep only final paper figures; exclude intermediate `page_images/` and layout checks. |
| Loss of git history in actor branch | Export the branch history but rewrite author/email if they contain host identifiers; otherwise keep it. |

## Migration Plan

1. Create `CodeGandee/isomer-example-fa4-example-model` with `gh repo create`.
2. Build a local staging copy of the public repo via export + sanitization script.
3. Push `main` branch, then push `actor-operator` branch.
4. In `main`, add `.gitmodules` and commit the submodule pointer to `actor-operator`.
5. Add `README.md`, `scripts/setup-extern.sh`, and reproduction instructions.
6. Run a validation pass: fresh clone, `pixi install`, `scripts/setup-extern.sh`, `pixi run test`, and paper build.

## Open Questions

- Should actor branches be squashed to a single public example commit, or should full history be preserved?
- Should `chatlogs/raw/` be excluded entirely, or summarized into a sanitized narrative file?
- Should the published repo include the NCU raw metrics CSVs, or only the analysis figures?
- Do we want a separate `isomer-example-fa4-analytical-model-actor-operator` repo instead of a branch-as-submodule?
