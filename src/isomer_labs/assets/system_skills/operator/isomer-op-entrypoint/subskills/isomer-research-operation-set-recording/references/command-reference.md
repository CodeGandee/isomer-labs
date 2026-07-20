# Command Reference

## Inspect

```text
isomer-cli --print-json ext research operation-sets inspect <operation-set-path> --topic <topic-id> --topic-actor <name>
isomer-cli --print-json ext research operation-sets inspect <operation-set-path> --topic <topic-id> --agent <name>
```

Add `--manifest-path <path>` to compare an explicit manifest inside the reserved control directory. Add `--write-scaffold` only to create a new incomplete default manifest. Inspection is otherwise read-only. A successful inventory can still return a failing reconciliation status until every disposition and binding is complete.

## Preview and Apply

```text
isomer-cli --print-json ext research operation-sets accept <manifest-path> --topic <topic-id> --topic-actor <name>
isomer-cli --print-json ext research operation-sets accept <manifest-path> --topic <topic-id> --topic-actor <name> --apply
```

Omit `--apply` for the required preview. Preview must return `mutated: false`, an ordered `actions` array, managed file plans, explicit parent and Idea effects, and `ok: true` before apply. Apply returns an acceptance header plus per-intent item states and verification output.

Use exactly one of `--topic-actor` and `--agent`. When both selectors are omitted, the command may infer one only if current context resolves exactly one worker.

## Verify

```text
isomer-cli --print-json ext research operation-sets verify <receipt-id> --topic <topic-id>
isomer-cli --print-json ext research operation-sets verify <operation-set-id> --topic <topic-id>
```

An operation-set id selects its latest receipt revision. Verify is read-only and never repairs missing records, files, lineage, or Research Idea effects.

## Result Interpretation

`applying` means an apply is in progress. `partial` means one or more items need safe resume while prior committed records remain durable. `complete` means every item committed and the coordinator's immediate verification succeeded. `superseded` preserves an earlier receipt after a later explicit revision completed.

Treat a nonzero command exit as incomplete closeout. Preserve the JSON diagnostic codes, manifest path, receipt id when available, failed intent key, and `recovery_actions` in the handoff.
