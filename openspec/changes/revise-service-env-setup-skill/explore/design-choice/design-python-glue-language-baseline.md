# Python Glue Language Baseline

## Decision

Every Topic Workspace root should keep Python as the baseline glue and orchestration language, regardless of the programming language required by the user-specified runnable target.

When no Python version can be recovered from the prompt, source gate, derived gate, or repo metadata, the setup workflow should choose the previous stable Python minor release relative to the latest stable Python release at execution time. When sources conflict, it should choose the highest Python minor version mentioned or required by those sources, then adapt environment-level requirements toward that version where service-safe.

## Rationale

Topic Workspace setup needs a stable scripting layer for inspecting repos, coordinating builds, preparing commands, running checks, and recording results. Python is the default orchestration language for that layer, even when the actual research or engineering target is C++, TypeScript, CUDA, Rust, shell, notebooks, or another language.

## Dependency Plan Impact

The generated `isomer-env-gate.md` should include Python as part of the Topic Workspace root environment, including the selected Python version, the evidence used to choose it, and any conflict-adaptation plan. For non-Python targets, the dependency plan should still add the native language toolchain, package manager, and runtime needed by the gate, while using Python only as the orchestration layer unless the target itself needs Python.

## Boundaries

Python as glue does not replace native toolchains. If the gate requires `cmake`, `node`, `pnpm`, `nvcc`, a browser runtime, or another non-Python tool, the setup workflow must still install and verify those tools through the appropriate Pixi/PyPI/channel choice.

Version adaptation must not mutate existing repo source files merely to force compatibility. If a conflict cannot be adapted through dependency selection, compatibility shims, or setup-command changes inside the service-safe setup boundary, the workflow should report a blocker with the conflicting sources and attempted target version.
