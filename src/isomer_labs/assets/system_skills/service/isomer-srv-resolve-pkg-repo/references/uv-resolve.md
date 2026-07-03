# uv Resolve

Use this subcommand to choose reachable Python package indexes for uv.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The Python package name(s) or requirement the user wants to install. |
| Project config | Optional `pyproject.toml` `[tool.uv]` `index-url` or `extra-index-url` entries. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test PyPI reachability** with `curl -I --max-time 10 https://pypi.org/simple/` or `uv pip install --dry-run --index-url https://pypi.org/simple/ <package>`.
2. **If PyPI is reachable**, recommend PyPI as the primary index.
3. **If PyPI is not reachable**, inspect user-home configuration for a preferred index. See **User Home Config Discovery**.
4. **If a user preference is found**, test it. If reachable, recommend that index and stop.
5. **If the user preference is not reachable**, report it as a blocker and stop. Do not silently fall back to another discovered source.
6. **If no user preference is found**, report that PyPI is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## User Home Config Discovery

Read uv and pip configuration from the user's home directory in this priority:

1. Environment variables: `UV_INDEX_URL`, then `PIP_INDEX_URL`, then `PIP_EXTRA_INDEX_URL`.
2. `~/.config/uv/uv.toml` — read `[tool.uv]` `index-url` and `extra-index-url`.
3. `~/.config/pip/pip.conf` — read `global.index-url` and `global.extra-index-url`.
4. `~/.pip/pip.conf` — read `global.index-url` and `global.extra-index-url`.
5. Project-local `pyproject.toml` `[tool.uv]` `index-url` or `extra-index-url` only when it is explicitly provided as context; do not search the filesystem for it.

Treat the first explicitly declared `index-url` as the user's preference. If only `extra-index-url` is declared, treat it as the preference only when no primary index is available.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

- `subcommand`: `uv-resolve`.
- `recommended_index_url`: the URL to pass to uv.
- `status`: reachable, blocked, or not tested.
- `blockers`: missing package context or no reachable index.

### Complete Output

- `pypi_reachable`
- `local_index_urls`
- `recommended_index_url`
- `tested_indexes`
- `blockers`
