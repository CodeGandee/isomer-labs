# Record Inspection Contract

Record inspection contracts feed record tabs, file artifact tabs, and supporting detail panels. The GUI uses lightweight descriptors first, then loads rendered content, files, lineage, siblings, and facets only when the relevant tab is open. Record detail tabs are Markdown-first: raw JSON belongs in the `View JSON` dialog.

## Viewer Descriptor Required Fields

- `ok`: whether the descriptor was produced.
- `mutated`: always `false`.
- `record_id`: record id.
- `viewer_kind`: viewer choice, such as `markdown`, `json`, `pdf`, `image`, `table`, or `unknown`.
- `exists`: whether the record exists in the read model.
- `diagnostics`: list of diagnostic objects.

Useful optional descriptor fields include `topic_id`, `title`, `primary_content_url`, `detail_url`, `render_url`, `files_url`, `facets_url`, `media_type`, `topic_workspace_relative_path`, `absolute_filepath`, `direct_parent_idea`, and `record_inspection`.

## Record Detail Display Fields

Record detail, render, or descriptor responses may expose:

- `topic_workspace_relative_path`: the artifact path relative to the Topic Workspace when the backend can derive it.
- `absolute_filepath`: the full local artifact filepath used by `Copy Filepath`.
- `direct_parent_idea`: compact structured metadata for the direct parent idea when known. Useful fields include `idea_id`, `display_key`, `title`, `summary`, `status`, and `source`.
- `record_inspection`: grouped display metadata that can repeat the path and parent idea fields.

The frontend should show relative path and direct parent idea under the record title when available. It should disable `Copy Filepath` when `absolute_filepath` is absent.

## Record Files Required Fields

A file list response must include `ok`, `mutated`, `topic_id`, `record_id`, `files`, and `diagnostics`. Each file item must include an `id` or `path`, `file_role`, `exists`, and `openable`. If `openable` is false, `open_blocked_reason` should explain why.

## Rendered and Supporting Payloads

Rendered record responses should expose a `render` object with content and diagnostics when Markdown is available. Lineage, siblings, files, facets, descriptor, detail, render, and diagnostics payloads are grouped into the record detail `View JSON` dialog. Lineage, siblings, and facets responses should keep their existing query-index shapes but include `ok`, `mutated`, and `diagnostics`.

## Extra Fields

Extra fields are allowed on descriptor, detail, file, lineage, sibling, facet, and render payloads. The GUI reads only the fields needed for tab selection, Markdown preview, metadata display, copy controls, and JSON modal grouping.

## Example

```json
{
  "ok": true,
  "mutated": false,
  "topic_id": "alpha",
  "record_id": "record-a",
  "title": "Experiment run",
  "viewer_kind": "json",
  "primary_content_url": "/api/topics/alpha/records/record-a/files/payload/content",
  "detail_url": "/api/topics/alpha/records/record-a",
  "files_url": "/api/topics/alpha/records/record-a/files",
  "media_type": "application/json",
  "topic_workspace_relative_path": "records/artifacts/record-a/payload.json",
  "absolute_filepath": "/project/topic-workspaces/alpha/records/artifacts/record-a/payload.json",
  "direct_parent_idea": {
    "idea_id": "idea-a",
    "display_key": "I-4",
    "title": "Experiment run idea",
    "source": "canonical_realization"
  },
  "exists": true,
  "diagnostics": []
}
```
