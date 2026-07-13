# npm Resolve

Use this subcommand to choose reachable registries for npm.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The package name(s) or scope the user wants to install. |
| Project config | Optional `.npmrc` in the project directory. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test the official npm registry** with `curl -I --max-time 10 https://registry.npmjs.org/` or `npm view <package> version`.
2. **If registry.npmjs.org is reachable**, recommend it.
3. **If the official registry is not reachable**, inspect local npm configuration:
   - Check `.npmrc` in the project directory, then `~/.npmrc`.
   - Read `registry`, `@<scope>:registry`, and `noproxy` entries.
4. **Test each candidate registry** in declaration order and recommend the first reachable one.
5. **If no registry is reachable**, report that registry.npmjs.org is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Recommend the registry URL for npm and state whether it is reachable, blocked, or untested. Name missing package context or the absence of a reachable registry as a blocker.

### Complete Output

Group the complete explanation by official-registry reachability, locally configured and tested registries, the recommendation, and blockers.
