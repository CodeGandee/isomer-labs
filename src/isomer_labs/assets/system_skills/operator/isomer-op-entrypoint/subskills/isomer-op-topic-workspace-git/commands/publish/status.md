# Publication Status

## Workflow

1. Resolve one registered Research Topic and Source Topic Workspace. Inspect Workspace Runtime when available but do not require it.
2. Load and validate runtime publication support when present. Otherwise inspect only a known or explicitly supplied Topic Publication Copy's ignored local support root. Do not find a copy by scanning Project temporary directories.
3. Validate binding identity, credential-safe locator, visibility, copy path, copy existence, projection manifest, current copy fingerprints, conflicts, semantic content classes, raw-byte settings, selected topic-owned components, selected GitHub references, reproduction limitations, per-branch outcomes, and safe resume point.
4. Verify that `README.md` and the portable research-record index exist and match their recorded fingerprints. Report the README latest-paper line, the exact selected paper Artifact ref and checksum when available, or the recorded absence or ambiguity.
5. Report `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked` without requiring or changing local tracking.
6. Do not contact the remote or promote copy-local support during read-only status. Report reconstruction inputs or the next plan or sync action.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only publication status plan and report the missing binding or selected context.
