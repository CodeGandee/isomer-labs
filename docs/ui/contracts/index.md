# Project Web UI Contracts

Project Web UI contracts describe the read-model payloads the local GUI needs to render Project and Topic Workspace views safely. They are UI read contracts, not canonical Workspace Runtime, query-index, or research-record storage schemas.

Agents and backend code may include fields beyond these contracts. Schema checks focus on required GUI fields and allow extra metadata so richer agent-produced records remain inspectable through `View JSON` and future viewers.

## Contract Pages

- [Topic Overview](topic-overview.md): topic overview Markdown, source metadata, supporting Topic and Runtime JSON, and missing-file diagnostics.
- [Topic Graph](topic-graph.md): graph identity, nodes, edges, groups, facets, renderer hints, paging, and diagnostics.
- [Idea Detail](idea-detail.md): canonical idea metadata, realizations, source provenance, source JSON availability, and lineage context.
- [Record Inspection](record-inspection.md): record viewer descriptors, rendered records, files, lineage, siblings, facets, and openability.
- [Diagnostics](diagnostics.md): common diagnostic fields and GUI rendering rules.
- [Display Paths](display-paths.md): topic-relative path labels used in status rows and file lists.

## Schema Policy

Python schemas under `src/isomer_labs/web/contracts/` validate the required fields named by these pages. They accept unknown top-level and nested fields unless a field conflicts with the type required by a current GUI view.

> Example: a graph node must include `id`, `record_id`, `material_kind`, `density_class`, and `title`, but it may also include agent-authored fields such as `confidence_notes`, `paper_section`, or `experimental_tags`.
