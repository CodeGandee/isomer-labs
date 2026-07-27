# Topic Workspace Publication Topology

## Status

accepted

## Scope

This exploration resolves how a Topic Publication Copy maps Source Topic Workspace paths, generated metadata, Topic Main and its worker-worktree snapshots, registered reference repositories, and publication branches into one inspectable remote repository.

## Evidence

- The canonical Topic Workspace path contract is semantic, and the Default Layout Profile is not mandatory.
- Topic Publication Copy is a disposable sanitized projection rather than a fourth workspace or canonical record source.
- Current projection inventory already preserves relative paths for normally discovered source files and component roots.
- The initial full publication diverged because an operator-generated mapping relocated root declarations under `environment/` and exposed Topic Main content at remote `main`.

## Resolved Choice: Structural Fidelity

Publication is a path-preserving subset of the Source Topic Workspace:

```text
source-backed retained path p  -> published path p
source-backed sanitized path p -> published path p with transformed bytes
selected nested repository p   -> exact gitlink at p
excluded path p                -> absent
empty directory                -> absent unless it contains a retained path
```

Publication must not group retained source content into synthetic content-class directories. Excluding private runtime, installed environments, credentials, temporary surfaces, or non-selected raw bytes does not permit relocation of any retained sibling.

## Acceptance Consequences

- Every source-backed `track`, `template`, or `component` entry has `output_relative_path == source_relative_path`.
- A mismatch blocks synchronization.
- Tests use both the default layout and a custom resolved layout.
- Publication-only generated files follow the minimal metadata overlay below and never relax source-path identity.

## Resolved Choice: Current-State Remote

The publication remote exposes only the current sanitized Topic Workspace state:

```text
main                  -> current sanitized Topic Workspace superproject
topic-workspace/main  -> absent
publication history   -> not a supported reproduction or rollback surface
```

The Source Topic Workspace and its durable records remain canonical. Publication commits are replaceable transport snapshots, so consumers must use the current manifest and pinned component commits rather than rely on publication ancestry.

## Current-State Consequences

- Remote HEAD selects `main`.
- Synchronization may replace prior publication commits instead of merging them.
- The old `topic-workspace/main` ref is removed rather than retained as an alias.
- Verification compares the complete current tree, gitlinks, and generated metadata.

## Resolved Choice: Persistent Exclusive-Snapshot Authority

Publication initialization records that the selected remote is dedicated exclusively to one Topic Workspace snapshot. That one-time acknowledgement authorizes subsequent approved syncs to replace or delete every Git ref and tag on the bound remote without separate destructive prompts.

Current-plan controls still apply:

- recompute the sanitized content selection and privacy result;
- inventory and fingerprint the complete remote ref and tag set;
- stop when the remote changes after planning;
- require new authorization if the remote identity, Topic Workspace identity, or snapshot mode changes.

Provider settings, issues, releases, packages, and other non-Git repository data are not covered by this Git snapshot authority.

## Resolved Choice: Same-Remote Topic Main Worktree Snapshots

Topic Main is the source Git anchor for Topic Actor Workspace and Agent Workspace worktrees. Publication removes machine-local worktree control files and represents the sanitized current tree of Topic Main and each selected worker worktree through replaceable branches in the same publication remote:

```text
main
components/topic-main
components/topic-actors/<sanitized-name>
components/agents/<sanitized-name>
```

Superproject `main` records each exact commit as a gitlink at the component's resolved Topic Workspace-relative path. Every topic-owned `.gitmodules` entry uses the same publication remote, and the Publication Projection Manifest identifies each actor or agent snapshot as anchored in Topic Main. The `components/...` namespace conveys snapshot transport rather than source ownership or historical lineage.

Registered third-party repositories do not use these branches. Their submodules retain normalized credential-free upstream GitHub locators and exact commits.

## Component Consequences

- Component snapshot refs are published before `main`.
- A recursive clone resolves every topic-owned component from the same publication remote.
- Each sync replaces component refs under the exclusive-snapshot authority.
- Topic Actor Workspace and Agent Workspace paths become ordinary submodule checkouts in the published clone, not local worktrees of `repos/topic-main`.
- Publication excludes source `.git` files, worktree administration data, absolute local paths, and source object databases.
- Source-style publication branches such as `topic-owner/main` and `per-topic-actor/<name>/main` are removed.
- Flattening component files into `main` is invalid.

## Resolved Choice: Publication Is Not a Topic Workspace Backup

The published repository is a sanitized evidence and artifact snapshot for inspection and reuse. It is not intended to restore an operational Topic Workspace, recreate Workspace Runtime, or reproduce local Git worktree mechanics automatically.

If a reader later wants a working Topic Workspace, that reader manually recreates the applicable Topic Workspace contract, including directories, Artifact placement, gitlinks, branch bindings, and worktrees. Publication provides paths, sanitized commits, and declarative relationships that can inform that work, but it provides no hydration command or restoration guarantee.

## Resolved Choice: Minimal Publication Metadata Overlay

Publication-generated tracked files use this layout:

```text
README.md
.gitmodules
.isomer-publication/
  research-record-index.json
  topic-workspace-projection.json
  topic-workspace-version.toml
```

Root `README.md` and `.gitmodules` are the only generated root exceptions. If a sanitizable source README exists, publication preserves its source-authored content outside a versioned generated navigation block. The latest-paper line links the eligible PDF at its path-preserved Artifact location rather than creating `paper/latest.pdf`.

## Metadata Consequences

- A source collision with `.isomer-publication/` blocks publication.
- Copy-local `.isomer/` support state remains untracked and distinct from the tracked overlay.
- Generated entries have explicit generated origin and cannot masquerade as source mappings.
- Root navigation remains immediately visible without scattering control files across the repository.

## Final Topology

```text
publication remote
├── main
│   ├── retained source-backed paths at identical relative paths
│   ├── repos/topic-main                  -> components/topic-main
│   ├── actors/<name>                     -> components/topic-actors/<name>
│   ├── agents/<name>                     -> components/agents/<name>
│   ├── registered third-party paths      -> exact upstream GitHub commits
│   ├── README.md
│   ├── .gitmodules
│   └── .isomer-publication/
├── components/topic-main
├── components/topic-actors/<name>
└── components/agents/<name>
```

All publication-owned Git refs and tags are current-state snapshot transport. The Source Topic Workspace and durable research records remain canonical, and a published clone is not an operational Topic Workspace.
