## MODIFIED Requirements

### Requirement: Research Record Browser APIs
The web service SHALL expose topic-scoped APIs for browsing indexed research records and canonical record details.

#### Scenario: List indexed records
- **WHEN** the frontend requests records for a Research Topic with optional filters
- **THEN** the API returns query-index record summaries using read-only Workspace Runtime access

#### Scenario: Export dashboard view
- **WHEN** the frontend requests a named export view such as `timeline`, `graph`, `dashboard`, `ideas`, `experiments`, or `claims`
- **THEN** the API returns query-index nodes, edges, files, ideas, routes, metrics, claims, facts, and diagnostics for that Topic Workspace

#### Scenario: Show record detail
- **WHEN** the frontend opens one record
- **THEN** the API returns lifecycle metadata and structured payload metadata and can include canonical payload JSON on request
- **AND** the response or associated viewer descriptor exposes Topic Workspace-relative path, absolute artifact filepath, and direct parent idea metadata when those values are available from structured records, query-index rows, or file metadata

#### Scenario: Render record Markdown
- **WHEN** the frontend requests rendered Markdown for a structured record
- **THEN** the API renders from the managed payload JSON and resolved Jinja2 template without writing a generated Markdown file

#### Scenario: Show record lineage and files
- **WHEN** the frontend requests lineage, files, or facets for one record
- **THEN** the API returns query-index derived data without repairing missing index rows
