# Discover Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:discovery-ledger` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/catalog/discovery-ledger/v1` | isomer-kaoju-discover | examine, audit, synthesize | Current discovery accounting | `derived_from` survey contract and prior ledger | Revise current ledger | catalog entries, source classes, cutoff, status |
| `kaoju:related-work-delta` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/catalog/related-work-delta/v1` | isomer-kaoju-discover | audit, synthesize | Direction-expansion or discovery delta | `derived_from` base catalog and seed works | Separate descendant per pass | additions, procedure, exclusions |
| `kaoju:curated-intake-delta` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/catalog/curated-intake-delta/v1` | isomer-kaoju-discover | audit, synthesize | User-nominated intake accounting | `derived_from` base survey and nominated identities | Separate descendant per intake | sources, source classes, dispositions |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-discover --producer 'isomer-kaoju-discover' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"<procedure>"}'
```

## Lifecycle

Validate payload-first with `records validate` and the row selectors, then create with **Normal Create**. List exact current or historical state with `records query list --artifact-family kaoju --semantic-id <id>` plus `--latest-only` when current state is required; show with `records show <record-id> --include-payload`; metadata-only changes use `records update`. Revise only the current ledger with `records revise`; create deltas as follow-up children with `--parents-json` and `--lineage-kind derived_from`. Render with `records render`; export via `records render --output-file`; archive with `records delete --reason`.
