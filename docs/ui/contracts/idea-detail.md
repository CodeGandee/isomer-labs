# Idea Detail Contract

The idea detail contract feeds the tab opened from a canonical Research Idea node. The GUI renders readable Markdown from `idea_content` or exact source JSON, and exposes raw JSON through the modal.

## Required Fields

- `ok`: whether the idea detail request succeeded.
- `mutated`: always `false` for this read model.
- `topic_id`: Research Topic id.
- `topic_workspace_id`: Topic Workspace id.
- `idea_id`: canonical Research Idea id.
- `idea`: canonical idea metadata object, or `null` if unavailable.
- `realizations`: list of Idea Realization objects.
- `generation_groups`: lineage generation groups.
- `incoming_edges`: parent lineage edges.
- `outgoing_edges`: child lineage edges.
- `source`: source JSON availability and provenance summary.
- `diagnostics`: list of diagnostic objects.

## Source Fields

`source` must include `source_kind`, `source_json_available`, `source_json_truncated`, and `source_json_bytes`. Optional source fields include `source_record_id`, `source_json_path`, `source_fragment_status`, `source_classification`, `payload_digest`, `payload_file_path`, `payload_media_type`, `full_source_url`, and exact `source_json`.

## Optional Useful Fields

- `exists`: whether the Research Idea exists.
- `latest_realization`: latest Idea Realization.
- `latest_record`: latest record metadata.
- `idea_content`: normalized idea content used for Markdown preview.
- `source_provenance`: compact source summary used in status rows.
- `error`: structured error object for missing ideas.

## Extra Fields

Extra fields are allowed. Agent-authored idea metadata may appear in `idea`, `idea_content`, realizations, lineage edges, or source JSON without breaking the GUI contract.

## Example

```json
{
  "ok": true,
  "mutated": false,
  "topic_id": "alpha",
  "topic_workspace_id": "alpha",
  "idea_id": "idea-a",
  "idea": {
    "idea_id": "idea-a",
    "title": "Launch-overhead correction",
    "status": "candidate"
  },
  "realizations": [
    {
      "idea_id": "idea-a",
      "record_id": "record-a",
      "latest": true
    }
  ],
  "generation_groups": [],
  "incoming_edges": [],
  "outgoing_edges": [],
  "idea_content": {
    "title": "Launch-overhead correction",
    "summary": "Separate host launch time from kernel runtime."
  },
  "source": {
    "source_kind": "latest_realization_source_path",
    "source_record_id": "record-a",
    "source_json_path": "$.sections.raw_ideas[0]",
    "source_json_available": true,
    "source_json_truncated": false,
    "source_json_bytes": 128
  },
  "diagnostics": []
}
```
