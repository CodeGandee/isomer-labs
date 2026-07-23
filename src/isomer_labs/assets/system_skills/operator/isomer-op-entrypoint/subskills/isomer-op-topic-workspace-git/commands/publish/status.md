# Publication Status

## Workflow

1. Resolve one registered Research Topic and Source Topic Workspace. Inspect Workspace Runtime when available but do not require it.
2. Load and validate runtime publication support when present. Otherwise inspect only a known or explicitly supplied Topic Publication Copy's ignored local support root. Do not find a copy by scanning Project temporary directories.
3. Validate binding identity, credential-safe locator, visibility, copy path, copy existence, projection manifest, current copy fingerprints, conflicts, selected components, per-branch outcomes, and safe resume point.
4. Report `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked` without requiring or changing local tracking.
5. Do not contact the remote or promote copy-local support during read-only status. Report reconstruction inputs or the next plan or sync action.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only publication status plan and report the missing binding or selected context.
