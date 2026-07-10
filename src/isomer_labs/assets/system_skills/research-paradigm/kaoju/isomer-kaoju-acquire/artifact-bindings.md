# Acquire Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below. Payloads contain locators and provenance, never material bytes.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:material-acquisition-manifest` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/material/material-acquisition-manifest/v1` | isomer-kaoju-acquire | workspace manager, examine, reproduce, compare | Current locator and availability inventory | `derived_from` source identities and owner results | Revise current manifest; separate observations | source class, access status, file and provenance refs |
| `kaoju:topic-dataset-manifest` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/material/topic-dataset-manifest/v1` | isomer-kaoju-acquire | workspace manager, reproduce, compare | Current dataset registry | `derived_from` external identity and Topic Workspace owner result | Revise after owner-confirmed change | dataset catalog, availability, source, file and provenance refs |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-acquire --producer 'isomer-kaoju-acquire' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"material-management"}'
```

## Lifecycle

Validate with `records validate`, then create with **Normal Create**. List with `records query list --artifact-family kaoju --semantic-id <id> --latest-only`; show with `records show <record-id> --include-payload`; use `records update` only for lifecycle metadata. Revise manifest content with `records revise <record-id> --semantic-id <id> --payload-file <payload-file>` after the owner returns immutable locator, managed-link, file, and provenance refs; create acquisition failures or observations as follow-up children. Render and export with `records render`, adding `--output-file` only for explicit export; archive with `records delete`. Never embed or delete external material.
