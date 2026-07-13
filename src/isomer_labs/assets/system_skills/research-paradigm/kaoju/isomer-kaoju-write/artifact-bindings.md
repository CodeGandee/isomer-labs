# Write Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:paper-contract` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/contract/paper-contract/v1` | isomer-kaoju-write | isomer-kaoju-pipeline, isomer-kaoju-write | Current target, scope, contribution posture, quality metrics, template ref, and validation policy | `derived_from` accepted audit and synthesis records | Revise current contract | target, venue, paper_type, template_name, status |
| `kaoju:survey-manuscript` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/manuscript/survey-manuscript/v1` | isomer-kaoju-write | isomer-kaoju-pipeline, isomer-kaoju-write | Current reader-facing paper view, evidence view, section jobs, citation ledger, `.tex` entry point, and included-file refs | `derived_from` paper contract and accepted survey records | Revise current manuscript | sections, claims, citations, template_name, status |
| `kaoju:paper-build-run` | Managed JSON snapshot | `run` | `topic.records.runs` | `isomer:research/record-format/profile/kaoju/run/paper-build-run/v1` | isomer-kaoju-write | isomer-kaoju-pipeline, isomer-kaoju-write | One immutable document-build attempt | `descendant_of` manuscript revision and prior build attempt when applicable | Immutable descendant | engine, template_digest, exit_status, output_refs |
| `kaoju:paper-validation-report` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/report/paper-validation-report/v1` | isomer-kaoju-write | isomer-kaoju-pipeline, isomer-kaoju-write | Non-mutating assessment of manuscript and build | `assesses` manuscript and build run | Immutable descendant | verdict, quality_profile, defects, warnings |
| `kaoju:publication-bundle` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/bundle/publication-bundle/v1` | isomer-kaoju-write | user and downstream research | Navigable assembly of accepted writing records and file refs | `assembled_from` accepted contract, manuscript, build, validation, and provenance records | Revise when manuscript or contract changes | bundle_refs, validation_verdict, status |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-write --producer 'isomer-kaoju-write' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"paper-writing"}' --parents-json '<accepted-input-refs>' --lineage-kind <row-lineage-kind>
```

## Lifecycle

Validate and create from accepted audited inputs. List exact family and semantic id, using `--latest-only` for current contract, manuscript, or bundle; show canonical payload; update only lifecycle metadata. Revise current-state content with `records revise`, preserve prior versions, and create separate build-run and validation-report descendants. Follow-up descendants replace prior build runs and validation reports. Render on demand and export explicitly; neither output becomes canonical evidence. Archive through generic record operations.
