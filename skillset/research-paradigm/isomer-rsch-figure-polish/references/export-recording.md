# Export Recording

Record enough information that another agent can find, inspect, regenerate, and interpret the final figure.

## Export Expectations

- `milestone`: normally PNG, with narrow message and linked Evidence Items.
- `paper_main`: PDF or SVG plus PNG preview; avoid rasterizing line art or text when vector output is possible.
- `appendix`: vector plus preview when practical.
- `review_response`: match the response package and link the reviewer item.
- `internal_review`: PNG or host-preferred preview is acceptable unless the figure may be promoted.

## Record Fields

- source data Artifact or Evidence Item path.
- figure-generation Artifact or script path.
- final export paths as figure output Artifacts resolved by Workspace Path Resolution.
- surface class.
- main Research Claim, comparison, report section, or reviewer item.
- visual inspection result.
- one short note on what changed during the self-review fix pass.
- remaining caveats, such as color risk, dense ticks, uncertain units, or unresolved export schema.

## Gate Conditions

Run Gate Policy preflight before final export when it involves cost, private data, credentialed services, external upload, venue-specific compliance, or irreversible publication-facing decisions, and open or record a Gate when the selected policy requires Operator Agent judgment.
