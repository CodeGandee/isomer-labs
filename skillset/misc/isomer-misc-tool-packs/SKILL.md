---
name: isomer-misc-tool-packs
description: Use only when explicitly invoked as isomer-misc-tool-packs or when the user directly asks to resolve a named installable toolset such as paper-writing, paper-figures-python, paper2ppt, cuda-build, torch-gpu, or topic-python-starter into dependency contracts, aliases, CLI-tool install routes, Python package install targets, verification checks, blockers, and downstream setup-skill handoff.
---

# Isomer Misc Tool Packs

## Overview

This manually invoked skill maps user-facing toolset names to setup contracts. It does not install dependencies; return the contract to the caller so that environment mutation, package-source evidence, enclosure, and verification stay with the setup owner.

## When to Use

Use this skill when the user explicitly invokes `isomer-misc-tool-packs` or directly asks to install, prepare, resolve, or inspect a named toolset, including prompts like `install toolset paper-writing`, `prepare paper figures`, `what does paper2ppt need`, `install torch-gpu tools`, or `resolve cuda-build tool pack`.

Do not route to this skill automatically from service, operator, or research workflow skills yet. Do not use this skill to install packages directly, mutate a Topic Workspace Pixi manifest, choose package mirrors, verify GPU runtime readiness, or inspect production DeepSci research-paradigm skills. Route those concerns to the owning service or misc skill named in the resolved contract only after the user chooses to act on the returned contract.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the requested toolset**:
   - Extract the user-facing toolset name or alias.
   - Normalize whitespace, underscores, and case to kebab-case.
   - If no toolset is named, list available canonical toolsets from `references/tool-packs.md`.
2. **Resolve the canonical pack**:
   - Read `references/tool-packs.md`.
   - Match the normalized name against canonical pack names and aliases.
   - If exactly one pack matches, continue.
   - If multiple packs match, report an ambiguity blocker and list candidate canonical names.
   - If no pack matches, report an unknown-toolset blocker and list available canonical names.
3. **Expand included packs**:
   - Include direct child packs named by the resolved pack.
   - Preserve the canonical root pack and the included pack list in the result.
   - Keep `paper-figures-r` opt-in; do not include it through `paper-writing`.
4. **Return the dependency contract**:
   - Include purpose, aliases matched, included packs, required tools, optional tools, dependency kind, install preference, package-source hints, host or external-tool expectations, verification checks, blockers, and helper-skill routes.
   - Distinguish command-line tools from importable Python packages.
   - For CLI tools distributed on PyPI, prefer `uv tool install <package>` when `uv` is available and PyPI has the package; fall back to `pixi global install <package>` when the uv tool route is unavailable, unsuitable, or does not expose the required command.
   - For importable Python packages or libraries needed by a topic runnable target, target the selected Topic Workspace Pixi environment.
5. **Hand off installation only when requested**:
   - Tell the caller that the returned contract can be recorded in `topic.env.topic_setup_target_spec` before dependency mutation when a Topic Workspace setup is active.
   - Leave actual installation and readiness verification with the setup owner, normally `isomer-srv-topic-env-setup`, after the user asks to proceed.
   - Route package-source, NVIDIA, PyTorch, or bounded-run concerns to the helper skills named in the contract.

If the request does not map cleanly to a known pack, use your native planning tool to infer the closest candidate only for explanation, then report a blocker rather than inventing a new canonical pack.

## Output Contract

Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

### Essential Output

Report:

- `status`: resolved, ambiguous, unknown, or blocked.
- `canonical_toolset`: resolved pack name when available.
- `matched_aliases`: aliases used by the request, if any.
- `includes`: included pack names.
- `required`: required tools grouped by dependency kind.
- `optional`: optional tools or fallback tools.
- `install_route`: CLI tool route and Python package target summary.
- `verification`: checks the setup caller should record.
- `routes`: helper skills to consult.
- `next_action`: usually ask whether to hand the contract to topic env setup or keep it as planning context.

### Complete Output

When requested, include:

- `canonical_toolset`
- `aliases`
- `matched_aliases`
- `purpose`
- `includes`
- `dependency_contract`
- `required_tools`
- `optional_tools`
- `package_source_hints`
- `host_or_external_tool_expectations`
- `verification_checks`
- `blockers`
- `helper_skill_routes`
- `setup_owner`
- `notes`

## Common Mistakes

- Installing directly from this misc skill instead of returning a contract to topic environment setup.
- Routing here automatically from service, operator, or research workflow skills before manual invocation is enabled.
- Treating a CLI tool distributed on PyPI as an importable project library.
- Installing importable Python libraries with `uv tool install` or `pixi global install` instead of the Topic Workspace Pixi environment.
- Including the R figure stack in `paper-writing` by default.
- Copying production DeepSci skill paths into this tool-pack catalog.
- Treating a successful package install as readiness without running the verification checks from the contract.
