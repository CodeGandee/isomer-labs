## 1. Self Query Foundations

- [x] 1.1 Add shared read-only self query helpers for Project discovery, Effective Topic Context, Topic Actor context, Effective Agent Context, selector handling, diagnostics, and side-effect-free payload assembly.
- [x] 1.2 Define subcommand-specific payload builders so `show`, `identity`, `pixi`, `env`, `paths`, and `queries` each return only their own slice.
- [x] 1.3 Ensure unresolved or conflicting Agent, Topic Actor, Topic, and Pixi inputs produce diagnostics without mutating state or guessing.

## 2. Subcommand Payloads

- [x] 2.1 Implement `project self show` as a minimal summary with selected topic/workspace headline, actor or agent headline when resolved, diagnostic counts, and available self subcommands.
- [x] 2.2 Implement `project self identity` with Effective Topic Context identity, Topic Actor context, Effective Agent Context, and source metadata only.
- [x] 2.3 Implement `project self pixi` with selected Pixi manifest path, Pixi environment, binding source, runnable `pixi run --manifest-path ... --environment ... python ...` hint, ambiguity diagnostics, and missing-binding diagnostics.
- [x] 2.4 Implement `project self env` with safe allowlisted Isomer environment names/classes/presence/influence by default, plus explicit safe-value output if supported, while omitting or redacting secret-like values.
- [x] 2.5 Implement `project self paths <label>...` so it requires at least one semantic label and resolves only requested labels.
- [x] 2.6 Implement `project self queries` with safe follow-up command examples and avoid embedding that full query catalog in other self subcommands.

## 3. CLI Command Surface

- [x] 3.1 Add the `project self` group and `show`, `identity`, `pixi`, `env`, `paths`, and `queries` subcommands to the root command-surface help and Click project command group.
- [x] 3.2 Implement deterministic JSON output for each subcommand with `command`, `output_schema_version`, `ok`, `mutated=false`, a subcommand-specific payload field, and `diagnostics`.
- [x] 3.3 Implement concise text output for each subcommand without printing broad environment, path, Pixi, or query detail blocks outside the requested slice.
- [x] 3.4 Support the existing topic, topic-workspace, lifecycle, agent-team-instance, agent-instance, topic-agent-team-profile, agent, and topic-actor selectors across the self subcommands using the same precedence and conflict behavior as existing context/path commands.

## 4. Topic Main Guidance and Documentation

- [x] 4.1 Update the topic-main guidance `.j2` template so `isomer-cli --print-json project self show` is the first recommended query.
- [x] 4.2 Add progressive examples for `project self identity`, `project self pixi`, `project self env`, and `project self paths <semantic-label>` while keeping lower-level `project context show`, `project paths get <semantic-label>`, and `project paths explain <semantic-label>` examples.
- [x] 4.3 Ensure the rendered guidance does not recommend a broad `project self --all`, `project self show --all`, or equivalent all-fields dump.
- [x] 4.4 Update `docs/isomer-cli.md` with `project self` subcommands, side-effect classification, JSON usage, environment variable guidance, and the token-light query pattern.
- [x] 4.5 Update any validator or fixture expectations that check the CLI command surface or topic-main guidance command list.

## 5. Tests

- [x] 5.1 Add CLI tests for `project self show --print-json` from Topic Main Development Repository cwd, verifying it is small and does not include detailed identity, env, path, Pixi, or query catalog payloads.
- [x] 5.2 Add CLI tests for `project self identity` from Topic Main Development Repository cwd with environment-provided Agent Instance or Agent Name, Agent Workspace cwd inference, Topic Actor context reporting, missing agent identity degradation, and environment/cwd conflict diagnostics.
- [x] 5.3 Add CLI tests for `project self env` safe allowlist reporting, default value omission, explicit safe-value behavior if implemented, and secret-like environment omission.
- [x] 5.4 Add CLI tests for `project self paths <label>...` requested-label-only behavior, missing-label diagnostics, and no full path catalog dump.
- [x] 5.5 Add CLI tests for `project self pixi` behavior with unambiguous Project-root bindings, standalone Topic Workspace binding/default, ambiguous bindings, and missing Pixi target diagnostics.
- [x] 5.6 Add topic-main guidance tests confirming `project self show` appears first, progressive self commands are shown, broad self dumps are not recommended, and no concrete topic-specific values are rendered.

## 6. Verification

- [x] 6.1 Run focused CLI tests for context, paths, self query, topic-main guidance, and docs/validator expectations.
- [x] 6.2 Run `pixi run python scripts/validate_skillsets.py`.
- [x] 6.3 Run `pixi run lint`.
- [x] 6.4 Run `pixi run typecheck`.
- [x] 6.5 Run `pixi run test`.
- [x] 6.6 Run `openspec instructions apply --change add-agent-self-query-command --json` and confirm all tasks are ready for implementation tracking.
