## Why

The packaged system-skill manager tells operators to pass `--json` to `project system-extensions list` and `remember`, but those subcommands accept structured-output selection only through the global `isomer-cli --print-json` option. The stale examples fail in the manager's required evidence and reconciliation workflows, so the package needs corrected guidance and an automated guard against recurrence.

## What Changes

- Replace the four stale system-skill manager examples with the supported global `isomer-cli --print-json ...` form.
- Extend packaged system-skill validation to reject command examples that place unsupported `--json` after an `isomer-cli` subcommand.
- Add regression coverage for both accepted global syntax and rejected command-local syntax.
- Verify the affected `list` and `remember` examples against their current CLI help and scan the packaged bundle for stale forms.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `packaged-system-skills`: Require packaged system-skill command examples to use the CLI's supported global structured-output option and require validation to reject stale command-local `--json` syntax.

## Impact

This change affects the system-skill manager Markdown references under `src/isomer_labs/assets/system_skills/`, the repository skillset validator in `scripts/validate_skillsets.py`, and its unit tests. It does not change CLI behavior or dependencies.
