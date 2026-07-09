# Recent Errors Contract

Recent errors are service-local Project Web diagnostics for graph and timeline interpretation. They help the GUI show recent non-interpretable data problems without reading log files or mutating Workspace Runtime data.

## Endpoint

`GET /api/topics/{topic_id}/recent-errors?limit=50`

The response is read-only. The buffer lives only in the running Project Web process, is bounded, returns newest entries first, and is cleared by service restart.

## Required Fields

- `ok`: whether the query succeeded.
- `mutated`: always `false`.
- `topic_id`: Research Topic id.
- `errors`: newest-first warning and error entries.
- `diagnostics`: diagnostics for the query itself.

## Error Entry Fields

Each entry includes `occurred_at`, `topic_id`, `source_view`, `severity`, `code`, and `message` when available. Useful optional fields include `idea_id`, `record_id`, and `details`.

## Example

```json
{
  "ok": true,
  "mutated": false,
  "topic_id": "alpha",
  "errors": [
    {
      "occurred_at": "2026-07-09T00:00:00Z",
      "topic_id": "alpha",
      "source_view": "graph:idea-lineage",
      "severity": "warning",
      "code": "idea_display_key_missing",
      "message": "Research Idea has no GUI display key: idea-a",
      "idea_id": "idea-a"
    }
  ],
  "diagnostics": []
}
```
