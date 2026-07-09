## Context

The `imsight-agent-skill-handling` skill is the manual entrypoint for analyzing, deep-inspecting, creating, testing, hardening, and formatting agent skills. It is maintained in `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-agent-skill-handling/`.

Currently, a designer who wants to understand what a proposed skill would look like must either:
- Run `create` and inspect the generated files, which mutates the filesystem.
- Manually draft a design document before asking an agent to implement it.

There is no subcommand that produces a planning artifact for human review without writing the skill files. Adding `design` closes this gap.

The Imsight skills suite defines a common output directory contract in `extern/orphan/houmao-agents/skillset/imsight-skills/README.md`: user-provided path, then `IMSIGHT_SKILL_OUTPUT_DIR`, then `<project-dir>/.imsight-arts/<subdir>`. The `design` subcommand will follow this contract and use its own `<subdir>`.

## Goals / Non-Goals

**Goals:**

- Add a `design` subcommand that generates a `design-overview.md` document from a user task.
- Make the default proposed skill a multi-subcommand skill with a `help` subcommand, because that shape is general enough to cover most cases.
- Teach the agent to follow the preferred skill format documented in `references/create.md` when drafting the proposed `SKILL.md` content inside the design document.
- Produce a deep-inspect-style process model: file inventory, concepts, high-level process, skill call graph, formal process, explanation, and evidence handoffs.
- Keep the output read-only and intended for human review; do not write actual skill files.

**Non-Goals:**

- Do not implement `design` as a dry-run mode of `create`.
- Do not generate actual `SKILL.md`, `agents/openai.yaml`, or other skill files.
- Do not install, validate against a runtime, or pressure-test the proposed skill.
- Do not change the behavior of existing subcommands (`analyze`, `deep-inspect`, `create`, `test`, `harden`, `format`).

## Decisions

### Default to multi-subcommand skill shape

- **Decision**: The `design` subcommand will default to designing a skill with multiple subcommands, including `help`.
- **Rationale**: A multi-subcommand skill is general enough to handle workflows that are procedural, collections of routines, or mixed. It also aligns with the Imsight convention that every `imsight-*` skill supports `help` and command-style invocation. The design document can downgrade to a single-command skill when the task clearly maps to a simple technique or pattern.
- **Alternatives considered**: Defaulting to single-command skills would be simpler but would require redesign when the task grows; defaulting to complex-procedure only would over-constrain peer-routine tasks.

### Output location under `.imsight-arts/skill-designs/`

- **Decision**: The default output directory is `<project-dir>/.imsight-arts/skill-designs/<slug-of-skill-name-no-more-than-6-words>/`, containing `design-overview.md`.
- **Rationale**: This follows the Imsight output contract and keeps design artifacts separate from analysis reports (`analyze`), process documents (`deep-inspect`), and created skill files (`create`). The slug truncation keeps paths readable.
- **Alternatives considered**: Reusing `.agent-skill-handling/deep-inspect/` would mix proposed-skill designs with inspected-skill analyses. Reusing `context/design/skill-process/` would overlap with `deep-inspect` output.

### Design document modeled on `deep-inspect.md`

- **Decision**: The generated document will use the same sections as `deep-inspect.md`: Purpose, File Inventory, Concepts, High Level Process, Skill Call Graph, Formal Skill Process, Skill Process Explanation, Evidence Handoffs, and Open Questions.
- **Rationale**: Designers are already familiar with this shape from `deep-inspect`. Using the same structure for proposed skills makes comparison easy and leverages existing tooling and mental models.
- **Alternatives considered**: A simpler outline would be easier to generate but would not expose subcommand routing and evidence handoffs, which are key for reviewing a proposed skill.

### No actual skill files produced

- **Decision**: `design` writes only `design-overview.md`.
- **Rationale**: The purpose is human review before implementation. Writing files would blur the line with `create`.
- **Alternatives considered**: Writing a draft `SKILL.md` alongside the design doc was rejected because it invites premature execution and confuses the output contract.

## Risks / Trade-offs

- **[Risk]** The design document may become long and hard to review if the agent generates too much pseudocode or too many subcommands.
  - **Mitigation**: Cap the default design to a small number of subcommands; document additional subcommands as "possible future extensions" when the task is broad.
- **[Risk]** Defaulting to multi-subcommand may over-design simple tasks.
  - **Mitigation**: The agent should explicitly justify the multi-subcommand choice in the design and offer a single-command alternative when the task is a pure technique or pattern.
- **[Risk]** The proposed skill name and description may be wrong or poorly scoped.
  - **Mitigation**: The design document includes open questions and asks the designer to confirm name, description, and scope before `create`.

## Open Questions

- Should `design` ask clarifying questions when intent is unclear, or should it make reasonable assumptions and document them as open questions?
- Should the formal process pseudocode use the same Agent-Primitive Python style as `deep-inspect.md`, or a lighter sketch?
- Should the design document include example prompts and expected AI responses for the proposed skill, or leave that to `create`?
