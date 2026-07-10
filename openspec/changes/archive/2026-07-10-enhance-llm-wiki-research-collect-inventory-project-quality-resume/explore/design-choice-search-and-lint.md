# Design Choice: imsight-llm-wiki Enhancement Search & Lint Behavior

## Questions Asked & Answered

| # | Question | Decision | Evidence |
|---|---|---|---|
| 1 | Which search provider should `research` use by default? | Provider-agnostic: native tool/skill first, CLI fallback, explicit failure message. | Avoids hardcoding Tavily; aligns with project having multiple search skills. |
| 2 | Should `collect` support local wiki search? | No — web-only external discovery, matching `nvk/llm-wiki` `/wiki:collect`. | `extern/orphan/llm-wiki/claude-plugin/commands/collect.md:156-159`. |
| 3 | Should quality-lint thresholds be configurable? | No default stale time; stale checks only run when user explicitly requests `--stale` or `--stale-days N`. | Staleness is context-dependent; avoids noisy defaults. |

## Resolved Behavior

- `research` discovers sources using whatever web-search capability is available to the agent, falling back to `tvly` or similar CLI tools, then ingests approved sources.
- `collect` uses web search to find external artifacts and writes a provenance-rich catalog to `wiki/collections/<slug>.md`.
- Enhanced `lint` runs overlength, orphan, and frontmatter checks by default; stale checks are opt-in.

## Updated OpenSpec Artifacts

- `openspec/changes/enhance-llm-wiki-research-collect-inventory-project-quality-resume/design.md` — decisions and open questions updated.
- `openspec/changes/enhance-llm-wiki-research-collect-inventory-project-quality-resume/specs/imsight-llm-wiki-collect/spec.md` — clarified web-only scope.
- `openspec/changes/enhance-llm-wiki-research-collect-inventory-project-quality-resume/specs/imsight-llm-wiki-quality-lint/spec.md` — stale check is now explicit.

## Suggested Next Action

Return to implementation planning. The OpenSpec change is now ready to apply; tasks may need minor updates to reflect the provider-agnostic search and opt-in stale checks.
