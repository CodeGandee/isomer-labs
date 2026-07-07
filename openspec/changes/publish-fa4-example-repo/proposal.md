## Why

The FlashAttention-4 white-box analytical model topic workspace is a self-contained research example (paper, predictor code, NCU validation, and actor work artifacts). Publishing it as a public GitHub repository under `CodeGandee/isomer-example-fa4-analytical-model` will provide a reproducible reference for the community and demonstrate the Isomer Labs research workflow. The workspace currently contains host-specific paths, large redownloadable artifacts, and private worktree state that must be sanitized before publication.

## What Changes

- Create a public GitHub repository `CodeGandee/isomer-example-fa4-analytical-model`.
- Implement a sanitization pass that masks host identity (`huangzhe`, `b200-14-hz`, local paths) in published files and git history.
- Strip or replace redownloadable/heavy content (`.pixi/`, `tmp/` simulators, `chatlogs/raw/`, caches, layout-check images).
- Convert upstream vendored repositories (`flash-attention`, `accel-sim-framework`) into proper Git submodules.
- Map the topic main repository and actor worktrees (`actors/operator`) to branches of the new repo, then expose the actor branches as submodules inside the main branch.
- Provide setup scripts and a README so a fresh clone can reproduce the environment and build the paper.

## Capabilities

### New Capabilities

- `example-repo-publication`: Sanitize, package, and publish a topic workspace as a public example repository while preserving its research artifacts and topology.
- `workspace-sanitization`: Mask host identity and remove non-portable or private workspace state before external publication.
- `actor-worktree-submodule`: Convert actor worktrees into branches of a public repository and re-attach them as Git submodules in the main branch.

### Modified Capabilities

- (none)

## Impact

- Affects the publication workflow and any scripts that produce or consume the public example repo.
- Does not change the source Isomer Labs project code or the existing topic workspace behavior.
- Introduces new utility scripts under `scripts/` in the published repo.
