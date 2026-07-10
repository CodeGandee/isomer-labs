# Synthesize Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:related-work-catalog` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/catalog/related-work-catalog/v1` | isomer-kaoju-synthesize | all survey stages and user | Current accepted work catalog | `derived_from` prior catalog, accepted deltas, digests, and audit | Revise current catalog | works, source classes, status, evidence refs |
| `kaoju:claim-status-table` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/report/claim-status-table/v1` | isomer-kaoju-synthesize | user and downstream research | Current audited conclusion status | `derived_from` accepted audit and claim-evidence ledger | Revise current table | claims, verdicts, status, evidence refs |
| `kaoju:field-summary` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/report/field-summary/v1` | isomer-kaoju-synthesize | user and downstream research | Bounded field synthesis | `derived_from` accepted catalog, comparisons, claim table, and audit | Revise from accepted deltas | claims, procedure, coverage cutoff |
| `kaoju:kaoju-dossier` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/report/kaoju-dossier/v1` | isomer-kaoju-synthesize | user and downstream research | Navigable assembly of accepted outputs | `derived_from` exact accepted survey records | Revise assembly when accepted inputs change | content catalog, procedure, record refs |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-synthesize --producer 'isomer-kaoju-synthesize' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"synthesis"}' --parents-json '<accepted-input-refs>' --lineage-kind derived_from
```

## Lifecycle

Validate and create from accepted audited inputs. List exact family and semantic id, using `--latest-only` for current catalog, claim table, summary, or dossier; show canonical payload; update only lifecycle metadata. Revise current-state content with `records revise`, preserve prior versions, and create separate follow-up evidence. Render on demand and export explicitly; neither output becomes canonical evidence. Archive through generic record operations.
