---
name: isomer-misc-pkg-specifics
description: Use when an Isomer Labs agent needs package-specific installation caveats, library source preferences, GPU/CPU variant checks, Pixi or PyPI package-selection warnings, named-package routing rules, or known setup traps for libraries such as PyTorch.
---

# Isomer Misc Package Specifics

## Overview

Use this skill as a compact index of package-specific installation caveats for Isomer Labs. Keep core environment setup skills generic; put library-specific preferences, traps, source-routing rules, and verification expectations here.

## When to Use

Use this skill when a task depends on a specific library whose package source, platform support, accelerator variant, build backend, or runtime check can change whether the environment is actually usable. Callers should check this skill before applying a generic PyPI, Conda, local-package, or system-Python source ladder.

Do not use this skill for generic Pixi mechanics, generic Python dependency installation, CUDA compiler preferences, or package-resolution policy that is not tied to a named package or library.

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

If the package is not listed, use your native planning tool to inspect official package docs or local package metadata, then report a concise package-specific note that can later become a new reference page.

## Packages

| Package | Use For | Detail |
| --- | --- | --- |
| `pytorch` | PyTorch package source, CPU/GPU variants, CUDA runtime support, Flash Attention builds, Triton compatibility, and model execution readiness | [references/pytorch.md](references/pytorch.md) |

## Common Mistakes

- Treating `import <package>` as proof that the required accelerator or runtime variant is installed.
- Installing an unqualified package name when the task requires a specific CPU, CUDA, ROCm, MPI, or platform variant.
- Recording a package as ready from solver success alone instead of checking the package's runtime metadata.
- Putting package-specific caveats in core service skills instead of this package-specific index.
