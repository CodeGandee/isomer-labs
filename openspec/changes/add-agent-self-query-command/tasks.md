## 1. Self Query Payload

- [ ] 1.1 Add a read-only self query helper that composes Project discovery, Effective Topic Context, Topic Actor context, Effective Agent Context, semantic path summaries, recognized safe `ISOMER_*` environment inputs, recommended follow-up commands, and diagnostics.
- [ ] 1.2 Implement safe environment reporting with an allowlist for identity/path/config refs and redaction or omission for credentials, tokens, passwords, API keys, and secret-like names.
- [ ] 1.3 Add Pixi binding summary logic that reports selected Project-root or standalone Topic Workspace Pixi manifest path, Pixi environment, binding source, and runnable `pixi run --manifest-path ... --environment ... python ...` hint when unambiguous.
- [ ] 1.4 Ensure unresolved or conflicting Agent, Topic Actor, Topic, and Pixi inputs produce diagnostics without mutating state or guessing.

## 2. CLI Command Surface

- [ ] 2.1 Add `project self show` to the root command-surface help and Click project command group.
- [ ] 2.2 Implement deterministic JSON output with `command`, `output_schema_version`, `ok`, `mutated=false`, `context`, `identity`, `environment`, `semantic_paths`, `pixi`, `recommended_queries`, and `diagnostics`.
- [ ] 2.3 Implement concise text output that summarizes resolved Research Topic, Topic Workspace, Topic Actor, Agent, Pixi hint, and follow-up query commands.
- [ ] 2.4 Support the existing topic, topic-workspace, lifecycle, agent-team-instance, agent-instance, topic-agent-team-profile, agent, and topic-actor selectors using the same precedence and conflict behavior as existing context/path commands.

## 3. Topic Main Guidance and Documentation

- [ ] 3.1 Update the topic-main guidance `.j2` template so `isomer-cli --print-json project self show` is the first recommended query.
- [ ] 3.2 Keep lower-level `project context show`, `project paths get <semantic-label>`, and `project paths explain <semantic-label>` examples in the rendered guidance.
- [ ] 3.3 Update `docs/isomer-cli.md` with `project self show`, side-effect classification, JSON usage, and environment variable guidance.
- [ ] 3.4 Update any validator or fixture expectations that check the CLI command surface or topic-main guidance command list.

## 4. Tests

- [ ] 4.1 Add CLI tests for `project self show --print-json` from Topic Main Development Repository cwd with environment-provided Agent Instance or Agent Name.
- [ ] 4.2 Add CLI tests for Agent Workspace cwd inference, Topic Actor context reporting, missing agent identity degradation, and environment/cwd conflict diagnostics.
- [ ] 4.3 Add CLI tests for safe environment allowlist reporting and secret-like environment omission.
- [ ] 4.4 Add CLI tests for Pixi hint behavior with unambiguous Project-root bindings, standalone Topic Workspace binding/default, ambiguous bindings, and missing Pixi target diagnostics.
- [ ] 4.5 Add topic-main guidance tests confirming `project self show` appears first and no concrete topic-specific values are rendered.

## 5. Verification

- [ ] 5.1 Run focused CLI tests for context, paths, self query, topic-main guidance, and docs/validator expectations.
- [ ] 5.2 Run `pixi run python scripts/validate_skillsets.py`.
- [ ] 5.3 Run `pixi run lint`.
- [ ] 5.4 Run `pixi run typecheck`.
- [ ] 5.5 Run `pixi run test`.
- [ ] 5.6 Run `openspec instructions apply --change add-agent-self-query-command --json` and confirm all tasks are ready for implementation tracking.
