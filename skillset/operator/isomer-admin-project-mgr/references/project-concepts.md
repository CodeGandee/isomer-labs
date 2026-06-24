# Project Concepts

An Isomer Project is a user-owned directory tree with a Project Config Directory at `.isomer-labs/`. The Project Manifest is `.isomer-labs/manifest.toml`; it is the discovery authority for Research Topics, Topic Workspaces, Domain Agent Team Template refs, Topic Agent Team Profile refs, and defaults.

A Research Topic is the root investigation intent. Its Research Topic Config normally lives at `.isomer-labs/research-topics/<topic-id>.toml`.

A Topic Workspace is the durable research workspace for one Research Topic. The default path created by `isomer-cli init <topic-id>` is `topic-workspaces/<topic-id>/`.

The Project-level Houmao overlay is `.houmao/` under the Project root. It supports Houmao-backed agent-team construction and management for the Project, but it is not a Workspace Runtime database or per-Agent Team Instance launch-material directory.
