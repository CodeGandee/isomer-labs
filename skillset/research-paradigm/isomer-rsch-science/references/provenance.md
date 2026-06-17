# Provenance

This skill adapts the DeepScientist `science` companion skill into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: scientific task classification, package availability checks, claim-type discipline, HPC and scheduler handling, task brief structure, domain routing, evidence recording, validation boundaries, and package-catalog deferral.

Source-runtime concepts were intentionally translated:

- source Science Evidence Graph language became linked Isomer Evidence Items, Artifacts, Research Claims, Validation Evidence Items, Decision Records, Gates, and Provenance Records.
- source command execution became Capability Binding through an Execution Adapter.
- source package cards became routing references that never prove runtime availability.
- source HPC-through-shell guidance became SSH, scheduler, queue, SLURM, log, and monitoring discipline through an Execution Adapter.
- source startup briefs became science-task brief Artifacts or handoff notes.
- source package-catalog generation was deferred instead of copied as a bulky generated resource.

The source package catalog drew routing ideas from the FermiLink skilled-scipkg channel. This Isomer adaptation does not vendor FermiLink runner code, CLI, service backends, package source trees, solver runtimes, or compiled executables.

License context: the DeepScientist source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
