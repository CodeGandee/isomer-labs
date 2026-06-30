# Deferred Resources

The DeepScientist source includes plotting scripts for eight paper-style reproductions. They were not imported into this Isomer skill bundle in this change.

## Decision

Defer script import.

## Rationale

- The scripts contain fixed paper-specific example data rather than reusable parameterized inputs.
- Several scripts write to absolute local paths from the source author's machine.
- Some scripts assume optional TeX or SciPy availability that the skill bundle cannot require as active behavior.
- The portable source value is the visual contract, data substitution discipline, and per-style routing, which are preserved in local references.

## Follow-Up Boundary

A later script-focused change may add sanitized generators under `scripts/` if each script accepts explicit input/output arguments, avoids source-local paths, records provenance, runs without unsatisfied hard dependencies, and writes through the accepted Isomer figure-output surface.
