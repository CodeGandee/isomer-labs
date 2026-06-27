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
3. **If PyPI is not reachable**, inspect local pip/uv configuration for declared index URLs. Check `UV_INDEX_URL`, `PIP_INDEX_URL`, `~/.config/pip/pip.conf`, `~/.pip/pip.conf`, and `[tool.uv]` in `pyproject.toml`.
4. **Test each candidate index** in declaration order and recommend the first reachable one.
5. **If no index is reachable**, report that PyPI is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## Output Contract

Report:

- `subcommand`: `uv-resolve`.
- `pypi_reachable`: `true`, `false`, or `not tested`.
- `local_index_urls`: URLs discovered from environment variables and config files.
- `recommended_index_url`: the URL to pass to uv.
- `tested_indexes`: each candidate and its reachability result.
- `blockers`: missing package context or no reachable index.
