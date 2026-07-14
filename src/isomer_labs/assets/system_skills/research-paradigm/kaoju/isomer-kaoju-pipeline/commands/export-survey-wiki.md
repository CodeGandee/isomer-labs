# Export Survey Wiki

## Workflow

1. Resolve an explicit Artifact subset or accepted direction and paper scopes through state-DB queries. Reject ambiguity and stale content.
2. Use `$isomer-kaoju-export` and only `isomer-cli ext kaoju wiki export` to render Markdown pages plus canonical JSON metadata.
3. Stage an idempotent in-place update at the Topic Workspace default or actor override. Replace only paths owned by the prior valid manifest, preserve human files, and report created, changed, unchanged, stale, and removed managed paths.
4. Register checksummed `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata` revisions.
5. On request, deploy the independently implemented installed-package viewer and register `kaoju:llm-wiki-viewer` plus its manifest. Clarify before touching a non-empty unrecognized target.
6. On request, start through `viewer_launch`, loopback by default. Handle port conflict, require a Gate for network exposure, and record Run and log refs.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-export`. Outputs: export, metadata, viewer, viewer manifest, changelog, Run, log, and local URL.

## Gates, Blockers, and Resume

Network exposure requires a human Gate. Missing accepted inputs, stale content, target ambiguity, protected files, port conflict, or launch failure records a blocker. Never invoke `imsight-llm-wiki`.
