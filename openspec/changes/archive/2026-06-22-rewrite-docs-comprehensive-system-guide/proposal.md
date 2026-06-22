## Why

The current `docs/` tree does not yet explain Isomer Labs as a coherent system, and `README.md` has become the only practical place where CLI behavior, architecture assumptions, and Houmao adapter usage are summarized. As Milestones 1 through 5 add Project discovery, Workspace Runtime, Agent Team Instance records, and Houmao-backed launch paths, users and future agents need comprehensive documentation that states what the system does, what it deliberately does not do, and how to operate it safely.

## What Changes

- Rewrite `docs/` into a documentation set that covers Isomer Labs concepts, system design, assumptions, intended usage, command workflows, runtime files, validation behavior, and troubleshooting.
- Add a complete `isomer-cli` command reference generated or checked against the installed Click command surface, including side-effect boundaries and JSON/text output expectations.
- Add system design documentation for Project discovery, Effective Topic Context, Workspace Path Resolution, Workspace Runtime, Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Houmao Execution Adapter behavior, manifest reconciliation, and current roadmap boundaries.
- Add an operator-focused usage guide that describes the normal path from Project initialization through topic readiness, profile validation, Agent Team Instance creation, prepare-only Houmao materialization, quick launch, inspect-live, stop, reconcile, and adopt.
- Add assumptions and non-goals documentation so users know which behavior is stable now, which behavior is intentionally adapter-specific, and which roadmap features are still future work.
- Add documentation verification tasks so docs stay aligned with canonical domain language, CLI help, README pointers, OpenSpec specs, and tests.
- Replace or reorganize ad hoc documentation under `docs/` while keeping `README.md` concise and redirecting readers to the detailed docs.

## Capabilities

### New Capabilities
- `isomer-documentation-system-guide`: Defines the comprehensive documentation contract for `docs/`, including system overview, CLI reference, design assumptions, intended usages, side-effect boundaries, Houmao adapter operation, troubleshooting, and verification.

### Modified Capabilities
- None.

## Impact

- Affected files: `docs/`, `README.md`, optional documentation helper scripts, and tests or checks that validate documentation coverage.
- Affected users: human operators learning Isomer Labs, contributors planning implementation work, and agentic maintainers that need a durable map of concepts, commands, runtime files, and safe workflows.
- Affected systems: documentation build or validation commands may be added, but no runtime CLI behavior or Workspace Runtime schema behavior is intended to change in this proposal.
