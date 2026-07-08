## Context

The current CLI has two install-shaped operations for Toolbox-related work. `project toolboxes install` writes a `[[toolboxes]]` registration row and manages Toolbox identity, source path, status, and scope. `project skill-callbacks install` loads the same Toolbox manifest and writes callback registry records, while also ensuring a matching Toolbox registration exists. Runtime-param definitions, imports, and overrides live under `project toolbox-params`.

That split matches the implementation layers, but it does not match the user model. A user who points at a Toolbox directory expects installation to make the Toolbox effective. At the same time, the lower-level surfaces are still valuable for users who have a callback prompt, a skill directory, or runtime-param defaults that are not yet packaged as a Toolbox.

The change should preserve the primitives while making `project toolboxes install` the canonical bundle operation.

```
                 canonical user path
                 ┌───────────────────────────┐
                 │ project toolboxes install │
                 └────────────┬──────────────┘
                              │
          ┌───────────────────┼────────────────────┐
          ▼                   ▼                    ▼
  register Toolbox     install callbacks     register defaults
  identity/status      from manifest          and validate params

          lower-level primitives stay available
          ┌────────────────────┐  ┌─────────────────────┐
          │ skill-callbacks ... │  │ toolbox-params ...  │
          └────────────────────┘  └─────────────────────┘
```

## Goals / Non-Goals

**Goals:**

- Make `project toolboxes install` install a Toolbox bundle, not just register its source/status row.
- Keep lower-level callback and runtime-param commands usable for loose/non-Toolbox material, migration, repair, and tests.
- Use the same scope language across Toolbox registration, callback install, and runtime-param configuration, while respecting that callback registry records currently support only Project and Research Topic scope.
- Preserve existing manifest schemas and registry storage formats unless a small additive field is needed for reporting.
- Report enough effective status after install for users and agents to understand what became active, skipped, gated, or invalid.

**Non-Goals:**

- Do not remove `project skill-callbacks register`, `resolve`, `list`, `show`, `disable`, or `validate`.
- Do not require all callback material to be packaged as a Toolbox.
- Do not add callback registry support for Topic Actor or Topic Agent scope in this change.
- Do not treat Toolbox runtime params as secrets or as automatic injected prompt text.
- Do not rewrite external Toolbox source directories during installation unless the user separately approves a fix.

## Decisions

### Make `project toolboxes install` the Bundle Orchestrator

`project toolboxes install <toolbox-dir>` should validate the Toolbox manifest, upsert the Toolbox registration, install declared callbacks, optionally register runtime-param default bundles, and report effective status. This matches the user phrase "install this Toolbox" and removes the need for users to know the internal split between registration and callback registry writes.

Alternative considered: keep `toolboxes install` registration-only and document the two-step workflow. That keeps implementation simple but preserves the confusing public shape that triggered this change.

### Keep `skill-callbacks install` as a Lower-Level Primitive

`project skill-callbacks install` should remain available as an explicit callback-manifest primitive. It is useful when a user or test wants to refresh callback records from a Toolbox manifest without changing runtime-param imports, when repairing a registry, or when migrating older callback bundles. Help text and docs should no longer present it as the normal way to install a Toolbox.

Alternative considered: remove or hide `skill-callbacks install`. That would simplify the public story but would remove a useful escape hatch and make migration/debugging workflows harder.

### Treat Runtime-Param Defaults as an Explicit Install Choice

Toolbox manifests can declare runtime params and default bundles, but installing those defaults mutates Project or Topic Workspace manifests. The high-level install should support a clear policy, such as installing default bundles when requested or when the command option explicitly opts in. The initial implementation should avoid silently adding runtime-param imports unless the install behavior is documented and visible in the output.

Alternative considered: always install every declared default bundle. That is convenient but risky because defaults can affect many callbacks across all topics when installed at Project scope.

### Normalize Scope Reporting Across Families

The high-level install output should use one vocabulary: Project-wide, Research Topic, Topic Actor, and Topic Agent. Internally, callback records can only be stored at Project or Research Topic scope for now. If a user selects Topic Actor or Topic Agent scope for a Toolbox install, the implementation should register Toolbox status/runtime params at that narrower scope and either install callbacks at the containing Research Topic scope or reject callback installation with a clear diagnostic until narrower callback storage exists.

Alternative considered: reject Topic Actor and Topic Agent scope entirely for Toolbox install. That would be simpler, but it would conflict with the runtime-param specialization model already present in Toolbox configuration.

### Report Effective Behavior, Not Just Mutation

After installation, the command should report installed callback ids, insertion points, Toolbox registration scope/status, runtime-param import rows, selected effective values when feasible, and diagnostics for gated callbacks or unavailable insertion points. This makes the command useful for agents as well as humans.

Alternative considered: return only written TOML rows and callback records. That is easier to implement but leaves the user unsure whether the installed Toolbox will actually participate in skill resolution.

## Risks / Trade-offs

- Bundle install may duplicate code from callback installation and runtime-param import handling -> Mitigation: factor shared service functions so `toolboxes install` orchestrates existing primitives rather than reimplementing validation and writes.
- Default runtime-param import behavior can surprise users at Project scope -> Mitigation: require explicit default-import policy and include defaults in the mutation summary before writing.
- Keeping `skill-callbacks install` may still look like a second Toolbox install path -> Mitigation: change help text and docs to describe it as a lower-level callback refresh/repair primitive.
- Topic Actor or Topic Agent Toolbox scope can imply callback specialization that callback registries do not support yet -> Mitigation: make output explicit that callbacks are registered at Project or Research Topic scope, while Toolbox status and runtime params may specialize more narrowly.
- Existing tests and docs may rely on `skill-callbacks install` as the primary Toolbox path -> Mitigation: keep compatibility while adding tests and docs for canonical `toolboxes install` behavior.

## Migration Plan

1. Refactor command handlers so `project toolboxes install` can call shared Toolbox manifest loading, callback installation planning, registration upsert, runtime-param import planning, and effective reporting services.
2. Preserve `project skill-callbacks install` behavior and JSON fields, but update help/docs to label it as a callback-manifest primitive.
3. Update specs and tests to assert that high-level Toolbox installation installs callbacks and registration together.
4. Update Toolbox Creator use cases and CLI docs to use `toolboxes install` for directories and lower-level commands only for loose callback/runtime-param material.
5. Rollback by keeping registration-only helper functions intact and limiting the high-level orchestration to the command handler path.

## Open Questions

- Should `project toolboxes install` install declared runtime-param default bundles by default, or require an explicit default-import option?
- Should Topic Actor and Topic Agent Toolbox install scopes install callbacks at the containing Research Topic scope, or should they reject callback installation until callback records support narrower scopes?
- Should `project skill-callbacks install` be renamed in a later breaking change to make its primitive role clearer, or is help/documentation enough?
