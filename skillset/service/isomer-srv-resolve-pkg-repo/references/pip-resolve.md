# pip Resolve

Use this subcommand to choose reachable Python package indexes for pip.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The Python package name(s) or requirement the user wants to install. |
| Project config | Optional `pip.conf` or environment `PIP_INDEX_URL` / `PIP_EXTRA_INDEX_URL`. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test PyPI reachability** with `curl -I --max-time 10 https://pypi.org/simple/` or `pip index versions <package>` when pip is available.
2. **If PyPI is reachable**, recommend PyPI.
3. **If PyPI is not reachable**, inspect user-home configuration for a preferred index. See **User Home Config Discovery**.
4. **If a user preference is found**, test it. If reachable, recommend that index and stop.
5. **If the user preference is not reachable**, report it as a blocker and stop. Do not silently fall back to another discovered source.
6. **If no user preference is found**, report that PyPI is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## User Home Config Discovery

Read pip configuration from the user's home directory in this priority:

1. Environment variables: `PIP_INDEX_URL`, then `PIP_EXTRA_INDEX_URL`.
2. `~/.config/pip/pip.conf` — read `global.index-url` and `global.extra-index-url`.
3. `~/.pip/pip.conf` — read `global.index-url` and `global.extra-index-url`.
4. `~/pip/pip.ini` — read `global.index-url` and `global.extra-index-url`.
5. `~/AppData/Roaming/pip/pip.ini` on Windows-style home layouts — read `global.index-url` and `global.extra-index-url`.

Treat the first explicitly declared `index-url` as the user's preference. If only `extra-index-url` is declared, treat it as the preference only when no primary index is available.

## Output Contract

Report:

- `subcommand`: `pip-resolve`.
- `pypi_reachable`: `true`, `false`, or `not tested`.
- `local_index_urls`: URLs discovered from environment variables and config files.
- `recommended_index_url`: the URL to pass to pip.
- `tested_indexes`: each candidate and its reachability result.
- `blockers`: missing package context or no reachable index.
