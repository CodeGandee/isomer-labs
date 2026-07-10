# Workspace Manager Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:workspace-readiness` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/control/workspace-readiness/v1` | isomer-kaoju-workspace-mgr | all Kaoju stages | Current readiness or blocker | `derived_from` checked context and binding index | Revise current state | readiness status, procedure, blockers |
| `kaoju:binding-index` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/control/binding-index/v1` | isomer-kaoju-workspace-mgr | all Kaoju stages | Current selected-skill binding coverage | `derived_from` semantic registry and selected binding pages | Revise current state | binding catalog and status |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-workspace-mgr --producer 'isomer-kaoju-workspace-mgr' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"workspace-bootstrap"}'
```

## Lifecycle

Validate with `records validate` and the row's record kind, semantic id, profile, skill, producer, consumer, actor metadata, and payload file; create with **Normal Create**. List with `records query list --artifact-family kaoju --semantic-id <id> --latest-only`; show with `records show <record-id> --include-payload`; use `records update <record-id> --record-kind <kind> --semantic-id <id>` only for metadata or lifecycle state. Revise content with `records revise <record-id> --semantic-id <id> --payload-file <payload-file>`; create follow-up evidence with **Normal Create** plus `--parents-json '[{"record_id":"<parent-id>","role":"input"}]' --lineage-kind derived_from`. Render on demand with `records render <record-id>`; export explicitly with `records render <record-id> --output-file <export-path>`; archive with `records delete <record-id> --reason <reason>`.
