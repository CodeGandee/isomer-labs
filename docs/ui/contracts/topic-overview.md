# Topic Overview Contract

The topic overview contract feeds the Project Web topic overview tab. The page renders `overview.content_markdown` as the main content and moves supporting JSON into the `View JSON` modal.

## Required Fields

- `ok`: whether the backend could resolve a usable topic overview response.
- `mutated`: always `false` for this read model.
- `topic_id`: Research Topic id.
- `topic_workspace_id`: Topic Workspace id, or `null` if the topic context is unavailable.
- `overview.semantic_label`: normally `topic.intent.overview`.
- `overview.exists`: whether the resolved Markdown file exists.
- `overview.content_markdown`: Markdown text when available, otherwise `null`.
- `topic_payload`: supporting Topic context JSON, or `null` when unavailable.
- `runtime_payload`: supporting Workspace Runtime JSON, or `null` when unavailable.
- `diagnostics`: list of diagnostic objects.

## Optional Useful Fields

- `overview.path`: resolved overview file path or locator.
- `overview.content_bytes`: byte size of the loaded Markdown file.
- `overview.content_cap_bytes`: backend read limit.
- `overview.path_display`: precomputed topic-relative display path, if provided.

## Extra Fields

Extra fields are allowed. The GUI reads the required fields above and keeps richer data available in JSON inspection.

## Missing File Behavior

When the overview file is missing, the response should stay usable: `ok` can remain `true`, `overview.exists` is `false`, `overview.content_markdown` is `null`, and `diagnostics` includes a stable warning such as `topic_overview_missing`.

## Example

```json
{
  "ok": true,
  "mutated": false,
  "topic_id": "flash-attention-4-whitebox-runtime-model",
  "topic_workspace_id": "flash-attention-4-whitebox-runtime-model",
  "overview": {
    "semantic_label": "topic.intent.overview",
    "path": "/project/isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/intent/src/topic-overview.md",
    "exists": true,
    "content_markdown": "# Topic Overview\n\nHigh-level intent.",
    "content_bytes": 39
  },
  "topic_payload": {
    "ok": true,
    "topic_config": {
      "topic_statement": "Model FlashAttention runtime."
    }
  },
  "runtime_payload": {
    "ok": true,
    "runtime": {
      "exists": true
    }
  },
  "diagnostics": []
}
```
