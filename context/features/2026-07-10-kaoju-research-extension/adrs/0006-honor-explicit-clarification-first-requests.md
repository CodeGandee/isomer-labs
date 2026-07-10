# Honor Explicit Clarification-First Requests

Status: accepted

When a user asks Kaoju to ask questions before starting a requested workflow, every Kaoju entrypoint shall enter a clarification-first checkpoint. The agent may inspect the prompt and already available context without mutation, but it shall not acquire materials, change environments, or begin a research Run until the user explicitly chooses to proceed.

## Considered Options

- Infer reasonable defaults and start immediately. This was rejected because it ignores the user's requested interaction boundary and may commit resources under the wrong scope.
- Ask broad free-form questions without proposed answers. This was rejected because it shifts the design burden to the user and hides the practical trade-offs.
- Present every possible ambiguity in one batch. This was rejected as the default because earlier answers may remove or change later questions; the clarification flow remains sequential unless the user requests a batch.

## Consequences

- Kaoju resolves questions answerable from the prompt and accepted project context before asking the user. It asks only about ambiguities that materially affect scope, evidence depth, source selection, comparison meaning, resource use, outputs, or acceptance criteria.
- Each clarification presents exactly four rows identified as A, B, C, and D. A, B, and C are three distinct concrete choices; D is `Say what you like` and accepts free-form input.
- The table includes the option, explanation, pros, and cons. Exactly one of A, B, or C is marked `Suggested`, with a brief evidence-based reason. When evidence is weak, Kaoju suggests the narrowest reversible choice and discloses that basis.
- Questions are asked one at a time. After integrating each answer, Kaoju asks: `Do you want to clarify more or proceed to execution?`
- `Clarify more` triggers another inspection of the remaining ambiguities and, when useful, the next structured question. `Proceed to execution` freezes the accepted decisions and visible assumptions, records the Proceed Decision, and starts the selected Kaoju pass when readiness and required Gates allow it.
- If no material ambiguity exists, Kaoju states that the request is ready and still asks whether the user wants to clarify more or proceed.
- In this interaction, `execution` means starting the selected Kaoju workflow. It does not imply that a source-only pass will run code, and it cannot bypass credentials, licenses, safety constraints, resource Gates, or missing authority.
