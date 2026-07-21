# System-Skill Manager Instructions Use Stale Command-Local `--json` Options

**Discovered**: 2026-07-21
**Last confirmed**: 2026-07-21
**Topic**: core operator system-skill management
**Severity**: documentation/workflow
**Status**: open

## What happened

While installing the Kaoju extension for Codex through `isomer-op-entrypoint->system-skills`, the loaded system-skill manager instructed the operator to run:

```text
isomer-cli project system-extensions list --json
```

The current CLI rejected that command with `No such option '--json'` and advised using the global output flag. The working form is:

```text
isomer-cli --print-json project system-extensions list
```

The same stale command-local option appears on the `project system-extensions remember` command. Its working JSON form is:

```text
isomer-cli --print-json project system-extensions remember <extension-id>
```

## Affected Instructions

The stale syntax appears in four places across three references:

- `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/subskills/isomer-op-system-skill-mgr/references/evidence-and-mutation.md`: `list --json` and `remember <extension-id> --json`
- `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/subskills/isomer-op-system-skill-mgr/references/detect-extensions.md`: `list --json`
- `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/subskills/isomer-op-system-skill-mgr/references/reconcile-extensions.md`: `remember <extension-id> --json`

The neighboring install and upgrade instructions already use the current global form, `isomer-cli --print-json ...`, which makes the reference bundle internally inconsistent.

## Why This Is a Problem

The stale command fails during the manager's required evidence ladder before installation or reconciliation. An agent must infer the correction from the CLI error, which adds an avoidable failed command and weakens confidence that the documented workflow matches the installed CLI. Automated consumers may stop at the failure instead of retrying with the global flag.

## Correct Intent

All system-skill manager instructions that request structured CLI output should place `--print-json` immediately after `isomer-cli`. Command-local `--json` should be removed unless a specific subcommand actually declares that option.

## Acceptance Criteria

1. Replace all four stale occurrences with the global `--print-json` form.
2. Confirm the affected list and remember examples against their current `--help` output.
3. Add or update a validation test that rejects command examples using unsupported command-local `--json` options in packaged system skills.
4. Verify the packaged skill bundle no longer contains `project system-extensions list --json` or `project system-extensions remember ... --json`.
