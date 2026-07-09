## 1. CLI Help Behavior

- [x] 1.1 Add a shared Click group helper that renders help and exits successfully when a command group is invoked without a child subcommand.
- [x] 1.2 Apply the shared group behavior to the top-level app, `project`, and every nested CLI command group.
- [x] 1.3 Replace the top-level long command dump with concise Isomer Labs overview text, repository and documentation links, and top-level command explanations.
- [x] 1.4 Add a root `--version` option that reports the installed package version.

## 2. Validation

- [x] 2.1 Add unit tests for top-level no-argument help, nested no-argument group help, and preservation of malformed-command diagnostics.
- [x] 2.2 Validate the OpenSpec change and run the focused CLI test coverage.
