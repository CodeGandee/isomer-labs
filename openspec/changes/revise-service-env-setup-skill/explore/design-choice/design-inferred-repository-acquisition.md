# Inferred Repository Acquisition

## Decision

`isomer-srv-env-setup` may infer, search for, and acquire independent repository sources when `env-gate.md` implies runnable code is needed but does not provide an explicit repository URL or local path.

## Rationale

The environment setup workflow should help the Topic Workspace become runnable, and many user gates will describe a desired command or package behavior without naming every required repository. Allowing repo source inference keeps the setup path useful for realistic, incomplete user intent.

## Warning Requirement

When the workflow acquires a repo from an agent-inferred source, the generated `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` must include a visible warning that the repository source was inferred rather than explicitly provided by the user. The warning should name the repo, expected path, inferred source, reason for choosing it, and any uncertainty or review needed. The final skill output should also report the warning.

## Boundaries

Inferred acquisition still places repos only under `<topic-workspace-dir>/repos/<repo-name>`. If the source remains ambiguous or the inferred repo cannot be verified against the desired command, the skill should report a blocker instead of claiming readiness.
