## Context

Topic environment setup already requires commands to run through the selected Topic Workspace Pixi environment. The missing rule is the command ordering for tools that themselves launch a target command, such as profilers, tracers, debuggers, and memory checkers.

The incorrect shape `<wrapper-tool> pixi run ...` launches Pixi as the profiled or debugged process. The intended shape is `pixi run <wrapper-tool> ... <target-command>`, so the wrapper tool and the target command resolve inside the same Pixi environment and Pixi does not become the measured process.

## Goals / Non-Goals

**Goals:**

- Make the wrapper-tool command-shape rule generic for Topic Workspace setup and verification.
- Ensure derived environment gates write replayable commands using `pixi run <wrapper-tool> ... <target-command>`.
- Ensure verification rejects or repairs obvious inverted commands such as `ncu pixi run ...`, `valgrind pixi run ...`, or `gdb --args pixi run ...`.
- Reinforce NVIDIA-specific examples for `ncu`, `nsys`, and `cuda-gdb`.

**Non-Goals:**

- Add a CLI command or schema field for command normalization.
- Build an automatic shell parser for arbitrary command strings.
- Change how Pixi manifests, dependencies, or workspace bindings are resolved.

## Decisions

1. Put the generic rule in `isomer-srv-topic-env-setup`.

   This skill derives and verifies Topic Workspace commands, so it is the closest common owner. Alternatives considered: only document the rule in NVIDIA guidance, or only add it to tutorials. Those options miss `valgrind`, `gdb`, and non-NVIDIA wrapper tools.

2. Add bounded-run reinforcement in `isomer-misc-bounded-run-tips`.

   Profilers and debuggers often appear in heavy or unknown-risk verification plans. Bounded-run guidance should preserve command ordering while selecting smaller inputs or shorter runs.

3. Keep NVIDIA-specific examples in `isomer-misc-nvidia-tools`.

   `ncu`, `nsys`, and `cuda-gdb` are common sources of the current mistake. The NVIDIA skill should provide concrete examples, but it should not own the generic rule.

4. Validate through skill-asset tests.

   Existing tests already inspect packaged system skill text for required guidance. Adding focused assertions is sufficient for this documentation-only behavior.

## Risks / Trade-offs

- Agents may still invert unknown wrapper tools not named in examples. Mitigation: describe the generic class as tools that execute a target command as a subprocess, then list representative examples.
- Overly strict wording could reject valid advanced use of Pixi under a debugger. Mitigation: allow exceptions only when local evidence proves that the target process must be Pixi itself.
- Command parsing remains human/agent-guided. Mitigation: use clear positive and negative command examples in the skills that author and verify commands.
