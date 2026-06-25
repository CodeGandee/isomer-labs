# Project Concepts

An Isomer Project is a user-owned directory tree with a Project Config Directory at `.isomer-labs/`. The Project Manifest is `.isomer-labs/manifest.toml`; it is the discovery authority for Research Topics, Topic Workspaces, Domain Agent Team Template refs, Topic Agent Team Profile refs, and defaults.

The default Project generated-content root is `isomer-content/`. Fresh initialization can select another project-local generated content root with `isomer-cli project init --content-dir <content-dir>`. Initialization writes `README.md` and `.gitignore` policy files inside the selected root; generated content under that root is ignored by default unless the user intentionally tracks selected files.

A Research Topic is the root investigation intent. Its Research Topic Config normally lives at `.isomer-labs/research-topics/<topic-id>.toml`.

A Topic Workspace is the durable research workspace for one Research Topic. `isomer-cli project topics create <topic-id> --statement "<research topic>"` creates the default path `isomer-content/topic-ws/<topic-id>/`; when Project init used `--content-dir <content-dir>`, topic creation derives `<content-dir>/topic-ws/<topic-id>/` instead.

The Isomer-managed Houmao Project directory is `.isomer-labs/`, passed to Houmao as `--project-dir`. The Isomer-managed Houmao overlay is `.isomer-labs/.houmao/`. It supports Houmao-backed agent-team construction and management for the Project, but it is not a Workspace Runtime database or per-Agent Team Instance launch-material directory. Root `.houmao/` is external user-owned Houmao state if present and must not be treated as Isomer-managed material.
