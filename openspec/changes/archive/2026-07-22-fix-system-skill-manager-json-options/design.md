## Context

Isomer exposes deterministic structured output through the root Click option `isomer-cli --print-json`. Four active system-skill manager references instead place `--json` after `project system-extensions list` or `remember`; Click rejects both forms before the documented evidence or reconciliation step can run. The packaged skill validator already scans active skill files for repository-local CLI invocation mistakes, so it is the narrowest shared enforcement point for this syntax rule.

## Goals / Non-Goals

**Goals:**

- Make every affected manager example executable with the current CLI.
- Reject exact command-local `--json` tokens in `isomer-cli` examples across packaged system skills.
- Preserve valid `--print-json` commands and unrelated options whose names merely end in `-json`, such as `--metadata-json`.

**Non-Goals:**

- Add a command-local `--json` compatibility alias to individual subcommands.
- Execute every documented command during validation.
- Generalize this change into a complete parser for shell or Markdown command examples.

## Decisions

1. Replace each stale example with `isomer-cli --print-json project system-extensions ...`. This matches the root option declared by the CLI and the neighboring install and upgrade guidance. Adding aliases to `list` and `remember` would expand the public CLI surface and leave the broader documentation convention inconsistent.
2. Extend the existing global `isomer-cli` invocation validator instead of adding a manager-only assertion. The manifest-catalog validation path already passes every packaged skill root to this validator, which protects all current and future public and protected skill pages.
3. Detect an exact `--json` token only within an `isomer-cli` command segment that does not start with `--print-json`. The matcher stops at common shell-command and Markdown delimiters so that it can inspect multiple commands on one line without confusing JSON-bearing options such as `--metadata-json` with the stale flag.
4. Cover the rule with focused validator tests for rejection and acceptance, then run the real packaged catalog validation and explicit stale-string scans. This provides a small unit-level regression and verifies the shipped bundle.

## Risks / Trade-offs

- [Risk] A regex-based command scan does not parse every possible shell construct. → Mitigation: keep the rule intentionally narrow to exact `isomer-cli` and `--json` tokens, stop at command delimiters, and test the supported and known stale forms.
- [Risk] Prose that intentionally documents the forbidden syntax could be flagged if it presents the text as an `isomer-cli` command. → Mitigation: describe the rule without placing both tokens in one command segment, or mark intentional fixtures outside packaged skill roots.
- [Risk] A future subcommand could legitimately add command-local `--json`. → Mitigation: the project-wide CLI convention reserves deterministic JSON for `--print-json`; any deliberate exception would require an explicit validator policy update with tests.
