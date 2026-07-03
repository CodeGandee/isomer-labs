# Codebase Audit Checklist

Use this only when attach/import/verify-local-existing is not enough and you truly need a fuller source audit.
Typical triggers are reproduce-from-source, repair with code changes, or an unclear evaluation entrypoint.

## Minimum audit coverage

Record:

- repository or package identity
- main entrypoints
- evaluation path
- data loading and preprocessing path
- configuration path
- metrics computation path
- output and checkpoint locations

## Implementation map

Identify:

- key classes and functions
- scripts that are likely to be run directly

## Practical constraints

Check:

- external services or downloads
- hardware assumptions
- brittle or undocumented environment requirements

## Baseline understanding goal

A later stage should be able to answer all of the following from your audit without reopening the entire repo:

- what the baseline does
- how it is run
- how it is evaluated
- where the main risks or bottlenecks are
