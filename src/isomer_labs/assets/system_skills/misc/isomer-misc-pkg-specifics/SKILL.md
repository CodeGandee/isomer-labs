---
name: isomer-misc-pkg-specifics
description: Use when an Isomer Labs agent needs package-specific installation caveats, library source preferences, GPU/CPU variant checks, Pixi or PyPI package-selection warnings, named-package routing rules, or known setup traps for libraries such as PyTorch.
---

# Isomer Misc Package Specifics

## Overview

- **Purpose**: provide a compact index of package-specific installation caveats for Isomer Labs.
- **Ownership**: keep library-specific preferences, traps, source-routing rules, and verification expectations here.
- **First lookup**: operational env gate derivation, package mutation, and package-specific runtime verification callers check this skill before applying generic PyPI, Pixi, Conda, local-package, system-Python, or generic verification rules for a named package.
- **Boundary**: core environment setup skills stay generic and route named-package caveats to this skill.

## When to Use

Use this skill when a task depends on a specific library whose package source, platform support, accelerator variant, build backend, or runtime check can change whether the environment is actually usable. Callers should check this skill before applying a generic PyPI, Conda, local-package, or system-Python source ladder.

Do not use this skill for generic Pixi mechanics, generic Python dependency installation, package-source reachability checks, bounded-run classification, CUDA compiler preferences, or package-resolution policy that is not tied to a named package or library.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the package-specific decision point**:
   - Name the package, library, runtime, platform, accelerator target, and the setup or verification step that depends on it.
2. **Use the package list**:
   - Select the relevant package from **Packages** when it exists.
   - Load only the selected package page.
   - If no listed package matches, report `no package-specific rule` and return control to the caller's generic package installation routing.
3. **Apply package-specific guidance**:
   - Use the package page to choose package source evidence, variant checks, verification commands, caveats, and blockers.
   - Keep the result scoped to the named package; do not turn this skill into a general environment setup guide.
4. **Report evidence back to the caller**:
   - Include package name, selected source or unresolved source, required variant, verification expectation, warnings, and blockers.

If the package is not listed, do not invent a package-specific rule inside the caller's workflow. Report `no package-specific rule`; the caller remains responsible for generic package routing, Pixi mutation, package-source reachability checks, bounded-run handling, env gate writing, and final readiness reporting.

## Packages

| Package | Use For | Detail |
| --- | --- | --- |
| `pytorch` | PyTorch package source, CPU/GPU variants, CUDA runtime support, Flash Attention builds, Triton compatibility, and model execution readiness | [references/pytorch.md](references/pytorch.md) |

## Common Mistakes

- Treating `import <package>` as proof that the required accelerator or runtime variant is installed.
- Installing an unqualified package name when the task requires a specific CPU, CUDA, ROCm, MPI, or platform variant.
- Recording a package as ready from solver success alone instead of checking the package's runtime metadata.
- Putting package-specific caveats in core service skills instead of this package-specific index.
- Turning this skill into a generic environment setup, package-source reachability, or bounded-run guide.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
