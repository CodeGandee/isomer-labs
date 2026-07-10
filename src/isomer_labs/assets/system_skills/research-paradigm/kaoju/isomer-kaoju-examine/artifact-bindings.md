# Examine Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:source-digest` | Managed JSON snapshot | `evidence_item` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/evidence/source-digest/v1` | isomer-kaoju-examine | compare, audit, synthesize | Exact source inspection evidence | `derived_from` immutable source identity and acquisition refs | Separate descendant for new identity or depth | claims, source class, verdict, depth, file refs |
| `kaoju:source-access-blocker` | Managed JSON snapshot | `evidence_item` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/evidence/source-access-blocker/v1` | isomer-kaoju-examine | pipeline, audit, user | Failed access evidence | `derived_from` requested source and attempted locators | Separate descendant per attempt | blocker status and source class |
| `kaoju:claim-evidence-ledger` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/evidence/claim-evidence-ledger/v1` | isomer-kaoju-examine | compare, audit, synthesize | Current claim-to-evidence map | `derived_from` source digests, Runs, and prior ledger | Revise current ledger | claims, verdicts, evidence refs, status |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-examine --producer 'isomer-kaoju-examine' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"source-examination"}'
```

## Lifecycle

Validate with `records validate`, create with **Normal Create**, list with `records query list --artifact-family kaoju --semantic-id <id>` and optional `--latest-only`, and show with `records show <record-id> --include-payload`. Use `records update` only for metadata; revise only the current ledger. Create each digest, blocker, deeper inspection, contradiction, or repair as a follow-up child with exact parents and `--lineage-kind derived_from`. Render with `records render`; export with `records render --output-file`; archive with `records delete --reason`.
