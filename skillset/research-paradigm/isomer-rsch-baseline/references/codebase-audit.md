# Codebase Audit

Use this only when attach, import, or verify-local-existing is insufficient and a fuller source/package audit is truly needed. Typical triggers are reproduce-from-source, repair with code changes, unclear evaluator, or unclear metric extraction.

## Minimum Audit Coverage

Record:

- repository, package, service binding, or local implementation identity
- main entrypoints
- evaluation path or Capability Binding
- data loading and preprocessing path
- configuration path
- metrics computation path
- output, checkpoint, or trusted-output locations as Evidence Item pointers
- expected resource class and material hardware assumptions
- external services, downloads, credentials, or data-export risks that require a Gate

## Implementation Map

Identify key classes, functions, scripts, notebooks, configuration files, or service handlers that a later stage may need to understand. Keep the map limited to the comparator route and metric contract.

## Practical Constraints

Check external downloads, service dependencies, credentials, hardware assumptions, brittle setup, undocumented environment requirements, and evaluator assumptions. Route concrete execution through a Capability Binding and use `[[tbd-surface:api-execution-command]]` when the command surface itself must be named.

## Baseline Understanding Goal

A later stage should be able to answer what the baseline does, how it is evaluated, where its trusted metrics came from, and where the main comparison risks remain without reopening the entire source package.
