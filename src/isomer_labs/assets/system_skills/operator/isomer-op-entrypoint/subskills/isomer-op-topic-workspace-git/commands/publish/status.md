# Publication Status

## Workflow

1. Resolve one registered Research Topic and Source Topic Workspace. Inspect Workspace Runtime when available but do not require it.
2. Load and validate runtime publication support when present. Otherwise inspect only a known or explicitly supplied Topic Publication Copy's ignored local support root. Do not find a copy by scanning Project temporary directories.
3. Validate binding identity, `exclusive_snapshot` authority, credential-safe locator, visibility, copy path, copy existence, projection manifest, current copy fingerprints, conflicts, semantic content classes, source-to-output path identity, raw-byte settings, selected topic-owned components, selected GitHub references, reproduction limitations, per-ref outcomes, observed remote HEAD, provider action state, and safe resume point.
4. Verify that `README.md` and `.isomer-publication/research-record-index.json` exist and match their recorded fingerprints. Report the README latest-paper line, the path-preserved selected paper Artifact ref and checksum when available, or the recorded absence or ambiguity.
5. Report `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked` without requiring or changing local tracking.
6. Do not contact the remote or promote copy-local support during read-only status. Report copy-recovery inputs or the next plan or sync action. State that publication recovery does not reconstruct an operational Topic Workspace.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only publication status plan and report the missing binding or selected context.
