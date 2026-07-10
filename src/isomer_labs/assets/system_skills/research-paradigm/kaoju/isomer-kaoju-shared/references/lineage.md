# Evidence Lineage

## Lineage Rule

Every derived Artifact names its direct inputs and the operation that derived it. Keep source discovery, source inspection, execution, comparison, audit, and synthesis as distinct lineage steps.

Minimum lineage includes:

- parent Artifact, Evidence Item, Run, or Decision Record refs;
- Source Identities and exact locators used;
- query, filter, transformation, patch, generator, or evaluator identity as applicable;
- actor and timestamp;
- Gate and Proceed Decision refs when applicable;
- output ref and status.

## Updates

Use a new Survey Delta, Evidence Item, Run, Finding, or Artifact version when meaning changes. Never overwrite an earlier source verdict with a repaired result, merge upstream and patched outputs, or detach a comparison cell from its underlying measurement.

## Failures

Failed and blocked work remains in lineage because it constrains interpretation. Record failure stage, attempted identity, logs or error evidence, effects on claims, and a bounded resume condition.
