# Diagnostics Contract

Diagnostics are GUI-safe messages that explain missing data, stale indexes, read errors, and contract validation failures. They should be specific enough for the GUI to group and display without requiring topic-specific code.

## Required Fields

No single diagnostic field is mandatory in every backend source, but GUI contract schemas accept diagnostic objects that may include `severity`, `code`, and `message`. Producers should provide all three when possible.

## Optional Useful Fields

Useful optional fields include `concept`, `path`, `field`, `hint`, `details`, `record_id`, `topic_id`, and `source`.

## Extra Fields

Extra fields are allowed. The GUI renders known summary fields and leaves detailed data available through JSON inspection.

## Contract Validation Failure

When backend UI contract validation fails at a read-model boundary, the response should include a diagnostic with code `gui_contract_validation_failed`, severity `error`, and a message naming the affected contract.

## Example

```json
{
  "severity": "warning",
  "code": "topic_overview_missing",
  "message": "Topic overview Markdown is missing.",
  "field": "topic.intent.overview",
  "hint": "Create the topic overview file before expecting the overview tab to show Markdown."
}
```
