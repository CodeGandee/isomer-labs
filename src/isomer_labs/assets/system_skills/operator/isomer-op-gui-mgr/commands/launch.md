# Launch GUI

## Workflow

1. Resolve the Project root from the prompt, current working directory, or explicit `--root` value.
2. Choose cache mode: `normal` for ordinary use, `debug` when browser cache may hide frontend or backend changes.
3. Build the launch command with `isomer-cli project web serve --root <project-root>`.
4. Add `--host`, `--port`, `--reload`, `--no-browser`, and `--cache-mode normal|debug` only when the user's request or debugging context calls for them.
5. Explain restart as stopping the existing foreground process or external process manager entry, then starting the command again.
6. Report the command, expected URL, cache mode, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a launch plan from the Project Web CLI options and local service guardrails, then execute the plan or report the missing input.

## Command Reference

Canonical launch:

```bash
isomer-cli project web serve --root <project-root>
```

Supported options:

- `--host <host>`: bind interface. The default is `127.0.0.1`.
- `--port <port>`: bind port. The default is `8765`.
- `--reload`: reload the web service when Python files change.
- `--no-browser`: do not open a browser automatically.
- `--cache-mode normal`: ordinary launch behavior with production cache practices.
- `--cache-mode debug`: no-store behavior for GUI shell, static assets, and API responses while iterating.

## Boundaries

The current CLI starts the GUI Backend. It does not provide `project web stop`, `project web restart`, `project web status`, or process logs. Use the terminal, tmux, shell job control, or the user's process manager for process lifecycle beyond start, and use `status` to inspect `/api/health` when a service URL is known.
