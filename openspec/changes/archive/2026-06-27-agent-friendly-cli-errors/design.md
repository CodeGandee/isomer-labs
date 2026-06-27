## Context

The installed script in `pyproject.toml` points `isomer-cli` at `isomer_labs.cli:main`. That function already runs Click with `standalone_mode=False`, which gives Isomer one place to intercept Click exits, Click exceptions, and unexpected Python exceptions. Normal command handlers already return through `emit_output(...)` and the `isomer-cli-output.v1` JSON wrapper, but Click usage errors currently call `exc.show()` directly and arbitrary exceptions can still escape as raw tracebacks.

Agents need failure output that answers four questions: what went wrong, which command shape was expected, what to try next, and whether mutation is known to have happened.

```text
argv
  |
  v
isomer_labs.cli.main
  |
  +-- Click command returns status ---------------> existing emit_output path
  +-- Click usage or parse error -----------------> invocation diagnostic
  +-- other ClickException -----------------------> CLI diagnostic
  +-- KeyboardInterrupt --------------------------> interrupted diagnostic
  +-- unexpected Python exception ----------------> internal-error diagnostic
```

## Goals / Non-Goals

**Goals:**

- Make every installed `isomer-cli` failure agent-readable by default.
- Preserve the existing successful command output contract.
- Return deterministic `isomer-cli-output.v1` JSON for failures when raw `argv` requests root-level `--print-json`.
- Include one to three valid examples for wrong-format invocations.
- Suppress raw tracebacks unless the caller explicitly opts into debug output.
- Keep examples and hints structured so agents do not need to parse prose.

**Non-Goals:**

- This change does not alter domain validation semantics for existing commands.
- This change does not redesign Click command registration.
- This change does not make command-local `--json`, `--format json`, or `--format=json` public invocation shapes.
- This change does not guarantee rollback for failures that happen after a mutating command has begun.

## Decisions

### Decision 1: The installed entrypoint owns failure normalization

`isomer_labs.cli.main` will become the safety boundary for installed CLI behavior. It will convert Click usage exceptions, non-usage Click exceptions, keyboard interrupts, and unexpected exceptions into Isomer diagnostics. Command handlers will continue returning normal payloads through `emit_output(...)`.

Alternative considered: wrap every command handler. That would miss parse errors, duplicate code across command modules, and still leave the installed script vulnerable to pre-dispatch failures.

### Decision 2: Diagnostics gain structured remediation fields

`Diagnostic` will gain optional structured fields such as `hint`, `usage`, and `examples`. JSON rendering will expose these fields as arrays or strings. Text rendering will print them after the primary diagnostic line in a stable order.

Examples are data, not prose embedded in `message`, because agents should be able to extract commands directly.

Alternative considered: append hints and examples into `message`. That keeps the dataclass smaller but forces agents to parse natural language and makes text/JSON output drift.

### Decision 3: Output mode is detected from raw argv for pre-dispatch errors

The failure renderer will scan raw `argv` for root-level `--print-json` before relying on Click context. This preserves JSON output for errors that happen before Click finishes parsing the root command. If no raw argument list is passed to `main`, the renderer will inspect `sys.argv[1:]`.

Alternative considered: depend on Click context for output mode. That fails for unknown root options, malformed command paths, and missing arguments before context propagation is complete.

### Decision 4: Command examples live in a registry keyed by command path

The CLI will keep a small registry of public examples keyed by command path, such as `project paths get` or `project topics create`. The invocation-error renderer will choose the nearest known command path from the Click context when available, with a raw-argv fallback for partial command paths.

The registry should reuse examples already documented in `docs/isomer-cli.md` to reduce drift. Each wrong-format diagnostic will include at most three examples.

Alternative considered: put example strings directly in exception-handling branches. That is simpler at first, but it scatters public invocation guidance and makes new commands easy to forget.

### Decision 5: Failure payloads report mutation certainty

Pre-dispatch invocation failures SHALL report `mutated: false`. Failures before command handler execution SHALL also report `mutated: false`. Unexpected exceptions caught after command dispatch may report `mutation_state: "unknown"` when the entrypoint cannot prove that no mutation occurred. Domain handlers that already know their mutation behavior keep using their existing `mutated` values.

Alternative considered: always set `mutated: false` on failures. That would be misleading for internal exceptions raised after a mutating command has already created or changed files.

### Decision 6: Tracebacks require explicit debug mode

Normal output will never include a Python traceback. Debug mode may be enabled by a root-level `--debug` option or by `ISOMER_CLI_DEBUG=1`. In text mode, debug output may include the traceback after the structured diagnostic. In JSON mode, debug details should live under a dedicated debug object so agents can ignore it safely.

Alternative considered: always include tracebacks in JSON because agents can parse them. That leaks implementation details, makes expected failures noisy, and weakens the user-facing contract.

## Risks / Trade-offs

- [Risk] Existing tests invoke `cli.app` directly and bypass `main`. → Add focused tests for `cli.main(...)` and keep direct Click tests only where they are intentionally testing command registration.
- [Risk] Example registry drifts from docs. → Seed examples from current documented command shapes and add docs validation or unit tests for the highest-value examples.
- [Risk] Internal exceptions after mutation cannot be classified perfectly. → Report `mutation_state: "unknown"` when the boundary lacks proof, and keep command handlers responsible for known domain failures.
- [Risk] Extending `Diagnostic` changes JSON shape. → Add only optional fields so existing diagnostics remain valid and older consumers that ignore unknown fields continue working.
- [Risk] Debug mode could accidentally leak sensitive values. → Keep debug opt-in explicit and preserve existing diagnostic discipline that reports fields and paths without printing secret values.

## Migration Plan

1. Extend diagnostics and rendering while keeping existing fields unchanged.
2. Add the failure renderer and route `main(...)` exceptions through it.
3. Add command examples for public command paths, starting with the commands already documented in `docs/isomer-cli.md`.
4. Add tests for missing argument, unknown command, invalid option, JSON parse failure output, internal exception normalization, and debug traceback opt-in.
5. Update CLI documentation to describe the failure contract and example behavior.

Rollback is straightforward because the change is isolated to the entrypoint and output helpers. Reverting the failure renderer restores Click's direct exception display, while command handler behavior remains unchanged.

## Open Questions

- Should debug mode be a root option, an environment variable, or both? The recommended implementation supports both so agents can opt in through command arguments and local developers can opt in through environment.
