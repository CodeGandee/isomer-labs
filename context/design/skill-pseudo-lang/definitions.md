# Skill Process Agent-Primitive Python Definitions

## Primitive Index

| Primitive | Meaning and Usage | Example |
| --- | --- | --- |
| `@skill(...)` | Declares a Python function as a named skill process entrypoint. Defines a skill node, but does not create a call edge. | `@skill(name="topic_team_specialization", description="Set up a specialized topic team.")` |
| `agent_do(...)` | Executes a vague natural-language task or transformation. Creates an agent service call node inside the current skill. | `agent_do("Summarize setup blockers for the operator.", context=setup_notes, returns=str)` |
| `agent_check(...)` | Evaluates a vague, qualitative, or semantic condition. Creates an agent judgment node inside the current skill. | `agent_check("Is the env gate concrete enough to run?", context=env_gate, returns=bool, rubric="True only when commands and success criteria are explicit.")` |
| `agent_select(...)` | Chooses among options by a qualitative criterion. Creates an agent selection node inside the current skill. | `agent_select(routes, criterion="Choose the route that best matches the user's requested proof.", context=user_request)` |
| `agent_invoke(...)` | Calls a named skill or agent service. Creates an explicit cross-skill call edge. | `agent_invoke("isomer-srv-topic-env-setup", task="Set up Topic Workspace env from env-gate.md.", context=topic_context, returns=StageResult)` |

## Purpose

This document defines a tiny Python-embedded language for describing skill processes. The design goal is not a new skill document language. It is ordinary Python with a small set of explicit agent-call primitives for the parts that require natural-language understanding.

The working name is Agent-Primitive Python. Python owns deterministic control flow, variables, functions, imports, dataclasses, file I/O, thresholds, loop bounds, and exact predicates. `agent_*` primitives represent intentionally vague service calls to an agent. This makes a skill process typed, inspectable, mockable, and composable while keeping the agent boundary visible in code.

## Core Rule

Use Python for everything Python can decide exactly.

```python
from pathlib import Path

if Path("user-intent/src/env-gate.md").exists():
    retry_budget = 3
else:
    retry_budget = 1

while plan_quality < 80 and attempts < retry_budget:
    attempts += 1
```

Use `agent_*` only when the operation is intentionally vague, qualitative, semantic, creative, or judgment-based.

```python
score = agent_check(
    "How practical is this cleanup plan for a small engineering team?",
    context=cleanup_plan,
    returns=int,
    scale=(0, 100),
    rubric="100 = immediately actionable; 70 = usable; 40 = vague; 0 = not useful.",
)
```

That is the boundary: Python handles formal predicates; agents handle fuzzy predicates.

## When to Use Python vs Agent Calls

| Use Python when | Use `agent_*` when |
| --- | --- |
| Checking whether a file exists. | Deciding whether a prose gate is usable enough to run. |
| Counting loop iterations. | Assessing whether evidence satisfies a natural-language requirement. |
| Comparing exact enum values. | Judging whether a plan is practical, coherent, or complete. |
| Sorting by a numeric cost. | Choosing among options by a qualitative tradeoff. |
| Reading a known key from a parsed object. | Reconciling partially inconsistent evidence across notes. |
| Calling a known local function with concrete arguments. | Invoking another skill for a bounded natural-language task. |
| Returning a dataclass or dictionary from a function. | Producing a natural-language summary, blocker explanation, or handoff note from messy context. |

Do not ask an agent to answer `x >= 10`, whether `Path("a.md").exists()`, or whether `round_count >= 100`. Write those checks directly in Python.

## Minimal Language

Agent-Primitive Python has one declaration helper and four agent-call primitives. Everything else is ordinary Python.

## Type Sketch

This sketch documents intended shape, not a committed runtime API.

```python
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Literal, TypeVar

T = TypeVar("T")
NL = str

Status = Literal[
    "ready",
    "changed",
    "blocked",
    "failed",
    "skipped",
    "not_checked",
    "deferred",
]


@dataclass(frozen=True)
class AgentAnswer(Generic[T]):
    value: T
    evidence: str | None = None
    confidence: float | None = None
    trace_id: str | None = None


@dataclass(frozen=True)
class StageResult:
    status: Status
    evidence: Sequence[str] = ()
    blockers: Sequence[str] = ()
    changed_refs: Sequence[str] = ()
    next_action: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


def skill(*, name: str, description: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    ...


def agent_do(
    task: str,
    *,
    context: object = None,
    returns: type[T] = str,
    constraints: str | Sequence[str] | None = None,
    rubric: str | None = None,
    evidence: bool = False,
) -> T | AgentAnswer[T]:
    ...


def agent_check(
    condition: str,
    *,
    context: object = None,
    returns: type[T] = bool,
    scale: tuple[int, int] | None = None,
    rubric: str | None = None,
    evidence: bool = False,
) -> T | AgentAnswer[T]:
    ...


def agent_select(
    options: Sequence[T],
    *,
    criterion: str,
    context: object = None,
    returns: type | None = None,
    evidence: bool = False,
) -> T | AgentAnswer[T]:
    ...


def agent_invoke(
    skill_name: str,
    *,
    task: str | None = None,
    context: object = None,
    returns: type[T] = str,
    params: Mapping[str, Any] | None = None,
    evidence: bool = False,
) -> T | AgentAnswer[T]:
    ...
```

By default, each primitive returns the requested Python value. When `evidence=True`, the runtime may return `AgentAnswer[T]` or record the evidence side channel in a trace store; the implementation must choose one convention and keep it consistent.

## Primitive Semantics

### `@skill`

Use `@skill` to mark a Python function as a skill-process entrypoint.

```python
@skill(
    name="topic_team_specialization",
    description="Set up a specialized topic team and orchestrate bounded setup stages.",
)
def setup_topic_team(topic_root: Path, user_request: str) -> StageResult:
    ...
```

Semantics:

- `@skill` gives the checker a stable skill name and description.
- `@skill` is not an agent call and is not a cross-skill call edge.
- A checker may use `@skill` metadata to build a skill graph, validate `agent_invoke` targets, and report entrypoints.

### `agent_do`

Use `agent_do` for vague task execution or transformation inside the current skill.

```python
summary = agent_do(
    "Summarize the architectural risks in this repository for a senior backend engineer.",
    context=repo_snapshot,
    returns=str,
)
```

Semantics:

- `task` is natural language and may require interpretation, synthesis, or transformation.
- `context` provides evidence or data, but exact data access and exact guards should remain in Python.
- `returns` should be `str` for prose or a concrete Python type for structured output.
- `constraints` and `rubric` narrow the agent's behavior when the task would otherwise be under-specified.
- `agent_do` should not perform irreversible side effects unless the task and constraints explicitly declare them.

### `agent_check`

Use `agent_check` for vague or qualitative judgment.

```python
is_clean = agent_check(
    "Is the public API easy to understand for a new contributor?",
    context=api_docs,
    returns=bool,
)
```

```python
score = agent_check(
    "How clean is the architecture?",
    context=repo_snapshot,
    returns=int,
    scale=(0, 100),
    rubric="0 = unmaintainable; 50 = workable but messy; 100 = clean, modular, documented.",
)

if score >= 70:
    status = "acceptable"
```

Semantics:

- Use `returns=bool` for yes/no semantic checks.
- Use `returns=int` or `returns=float` for graded judgments, and always provide `scale`.
- Provide `rubric` when a result will drive a branch, threshold, mutation, or cross-skill call.
- Do not use `agent_check` for deterministic comparisons, exact enum checks, file existence checks, or loop counters.

### `agent_select`

Use `agent_select` for qualitative choice among options.

```python
best_refactor = agent_select(
    candidate_refactors,
    criterion="Choose the option with the best tradeoff between simplicity, risk reduction, and implementation cost.",
    context=repo_snapshot,
)
```

Semantics:

- `options` should be explicit values the caller can inspect and test.
- `criterion` is natural language because the choice depends on judgment.
- Use ordinary Python for deterministic selection.

```python
cheapest = min(options, key=lambda option: option.cost)
```

### `agent_invoke`

Use `agent_invoke` to call a named skill or agent service inside the process graph.

```python
topic_env = agent_invoke(
    "isomer-srv-topic-env-setup",
    task="Set up Topic Workspace environment from env-gate.md without reading agent-env-gate.md.",
    context=topic_context,
    returns=StageResult,
    params={
        "subcommand": "setup-topic-env",
        "orchestrator": "isomer-admin-topic-team-specialize",
    },
)
```

Semantics:

- `agent_invoke` is the only primitive that creates a top-level cross-skill call edge.
- The caller remains responsible for orchestration after the invoked skill returns.
- A returned `next_action` string is advisory; it is not a call graph edge.
- The invoked skill returns typed evidence or blockers; it should not silently continue into another top-level skill unless the process explicitly permits that.
- `params` carries structured boundary metadata such as subcommand, orchestrator, allowed refs, forbidden refs, and expected outputs.

## Typed Return Objects

For anything more complex than prose, use Python types.

```python
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Finding:
    severity: Literal["low", "medium", "high"]
    title: str
    evidence: str
    recommendation: str


@dataclass(frozen=True)
class Review:
    score: int
    summary: str
    findings: list[Finding]
```

```python
review = agent_do(
    "Review this codebase architecture for modularity, coupling, cohesion, naming, ownership boundaries, and change risk.",
    context=repo_snapshot,
    returns=Review,
    rubric="""
    score 90-100: clean, modular, easy to evolve
    score 70-89: acceptable with minor design debt
    score 40-69: meaningful architectural problems
    score 0-39: severe coupling or unclear boundaries
    """,
)

if review.score < 70:
    plan = agent_invoke(
        "refactoring_plan",
        task="Create a pragmatic staged cleanup plan for the architectural findings.",
        context=review,
        returns=str,
    )
```

The threshold logic is deterministic Python. The review and plan creation are semantic agent calls.

## Example: Team Specialization Process

This example mirrors the intended Isomer topic-team setup flow. Python checks exact file existence and exact status values. Agent primitives handle semantic setup work, evidence judgment, and cross-skill invocation.

```python
from pathlib import Path


@skill(
    name="isomer-admin-topic-team-specialize",
    description="Specialize a Research Topic team and orchestrate workspace, topic env, and agent env setup.",
)
def setup_topic_team(topic_root: Path, user_request: str) -> StageResult:
    topic = agent_do(
        "Resolve or create the registered Research Topic and Topic Workspace, then specialize the selected Domain Agent Team Template.",
        context={"topic_root": topic_root, "user_request": user_request},
        returns=StageResult,
        constraints=[
            "Produce authoritative Agent Names when available.",
            "Do not launch runtime teams.",
        ],
    )
    if topic.status in {"blocked", "failed"}:
        return topic

    workspace = agent_invoke(
        "isomer-admin-topic-workspace-mgr",
        task="Prepare Topic Workspace and Agent Workspace Git topology for the specialized topic team.",
        context={"topic": topic, "user_request": user_request},
        returns=StageResult,
        params={
            "subcommand": "setup-topic-workspace",
            "expect": ["Topic Main Repository", "Agent Workspace paths", "branch plan", "Git topology validation"],
            "must_not_call": ["isomer-srv-agent-env-setup"],
        },
    )
    if workspace.status in {"blocked", "failed"}:
        return workspace

    env_gate = topic_root / "user-intent/src/env-gate.md"
    if env_gate.exists():
        topic_env = agent_invoke(
            "isomer-srv-topic-env-setup",
            task="Set up Topic Workspace environment from env-gate.md.",
            context={"topic": topic, "workspace": workspace, "env_gate": env_gate},
            returns=StageResult,
            params={
                "subcommand": "setup-topic-env",
                "expect": ["isomer-env-gate.md", "Topic Workspace Pixi readiness", "dependency and enclosure evidence"],
                "must_not_read": ["user-intent/src/agent-env-gate.md"],
                "must_not_write": ["user-intent/derived/isomer-agent-env-gate.md"],
                "must_not_call": ["isomer-srv-agent-env-setup"],
            },
        )
        if topic_env.status in {"blocked", "failed"}:
            return topic_env
    else:
        topic_env = StageResult(
            status="not_checked",
            blockers=["No env-gate.md exists."],
            next_action="Ask whether Topic Workspace environment setup is needed.",
        )

    agent_env_gate = topic_root / "user-intent/src/agent-env-gate.md"
    if agent_env_gate.exists():
        agent_env_inputs_ready = agent_check(
            "Do the existing topic-team, workspace topology, and topic env evidence satisfy the prerequisites for agent env setup?",
            context={"topic": topic, "workspace": workspace, "topic_env": topic_env, "agent_env_gate": agent_env_gate},
            returns=bool,
            rubric="True only when agent-env-gate.md exists, Git topology evidence exists, Topic Workspace predecessor evidence is ready or explicitly deferred, and authoritative Agent Names are known.",
        )
        if not agent_env_inputs_ready:
            return StageResult(
                status="blocked",
                blockers=["Agent env setup prerequisites are not satisfied."],
                evidence=[str(agent_env_gate)],
                next_action="Repair missing topic env, workspace topology, or Agent Name evidence before setup-agent-env.",
            )

        agent_env = agent_invoke(
            "isomer-srv-agent-env-setup",
            task="Set up and verify Agent Workspace cwd readiness from agent-env-gate.md using existing Topic Workspace env evidence.",
            context={"topic": topic, "workspace": workspace, "topic_env": topic_env, "agent_env_gate": agent_env_gate},
            returns=StageResult,
            params={
                "subcommand": "setup-agent-env",
                "expect": ["isomer-agent-env-gate.md", "readiness by Agent Name", "overall agent readiness"],
                "must_not_call": ["isomer-srv-topic-env-setup"],
            },
        )
        if agent_env.status in {"blocked", "failed"}:
            return agent_env

    return StageResult(
        status="ready",
        evidence=[
            "topic-team setup evidence",
            "workspace topology evidence",
            "topic env evidence when checked",
            "agent env evidence when checked",
        ],
        next_action="Run validate-topic-team.",
    )
```

The important process rule is visible in the code: topic env setup does not care whether each Agent Workspace passes `agent-env-gate.md`; agent env setup owns that concern, and the team-specialization skill orchestrates when to call it.

## Static Checker

The checker should not try to prove that an agent answer is true. It should check the shape of the skill call graph and the discipline of agent boundaries.

Python's `ast` module can parse skill source into an abstract syntax tree. A checker can extract `@skill` declarations, Python branch expressions, `agent_*` calls, assignments, `agent_invoke` targets, and data dependencies.

Example extracted shape:

```json
{
  "skill": "isomer-admin-topic-team-specialize",
  "python_branches": [
    "if topic.status in {'blocked', 'failed'}",
    "if env_gate.exists()",
    "if agent_env_gate.exists()",
    "if not agent_env_inputs_ready"
  ],
  "agent_calls": [
    {
      "primitive": "agent_do",
      "task": "Resolve or create the registered Research Topic...",
      "returns": "StageResult",
      "assigned_to": "topic"
    },
    {
      "primitive": "agent_invoke",
      "skill_name": "isomer-admin-topic-workspace-mgr",
      "returns": "StageResult",
      "assigned_to": "workspace"
    },
    {
      "primitive": "agent_invoke",
      "skill_name": "isomer-srv-topic-env-setup",
      "returns": "StageResult",
      "assigned_to": "topic_env"
    },
    {
      "primitive": "agent_check",
      "condition": "Do the existing topic-team, workspace topology, and topic env evidence satisfy the prerequisites for agent env setup?",
      "returns": "bool",
      "assigned_to": "agent_env_inputs_ready"
    },
    {
      "primitive": "agent_invoke",
      "skill_name": "isomer-srv-agent-env-setup",
      "returns": "StageResult",
      "assigned_to": "agent_env"
    }
  ],
  "call_edges": [
    ["isomer-admin-topic-team-specialize", "isomer-admin-topic-workspace-mgr"],
    ["isomer-admin-topic-team-specialize", "isomer-srv-topic-env-setup"],
    ["isomer-admin-topic-team-specialize", "isomer-srv-agent-env-setup"]
  ]
}
```

That extraction is enough for consistency checks without building a heavy runtime.

## Lint Rules

Use lint rules to preserve the Python/agent boundary.

```text
A001 agent_check returning int or float must declare scale=(min, max).
A002 agent_check used in a threshold comparison should provide a rubric.
A003 deterministic comparisons should not be delegated to agent_check.
A004 agent_do or agent_invoke returning non-str should declare a return type.
A005 an agent result passed into another agent call should have a named variable, not a deeply nested call.
A006 loops controlled by agent outputs must have a deterministic bound.
A007 agent_do should not perform irreversible side effects unless the task and constraints explicitly declare them.
A008 agent_invoke skill_name must resolve to a known skill.
A009 agent_check returning bool should ask a yes/no question.
A010 agent_select should only be used when the choice criterion is qualitative.
A011 only agent_invoke creates a top-level skill call edge.
```

Warning example:

```python
if agent_check("Is x >= 10?", context=x, returns=bool):
    ...
```

The checker should warn:

```text
A003: This appears deterministic. Use `if x >= 10:` instead of `agent_check`.
```

Loop warning example:

```python
while agent_check("Is the answer good enough?", context=answer, returns=bool):
    ...
```

The checker should warn:

```text
A006: Loop depends on an agent judgment and has no deterministic bound.
```

Better:

```python
attempts = 0
answer_ok = agent_check("Is the answer good enough?", context=answer, returns=bool)

while not answer_ok and attempts < 3:
    answer = agent_do("Improve the answer.", context=answer, returns=str)
    answer_ok = agent_check("Is the answer good enough?", context=answer, returns=bool)
    attempts += 1
```

## Runtime Model

At runtime, each `agent_*` call is a typed RPC to an agent service.

```python
agent_call = {
    "primitive": "agent_check",
    "task": "How clean is the architecture?",
    "context": repo_snapshot,
    "returns": int,
    "scale": [0, 100],
    "rubric": "0 = unmaintainable; 100 = clean, modular, documented.",
}
```

The agent service may return value plus trace metadata:

```python
agent_return = {
    "value": 64,
    "evidence": "The codebase has cyclic dependencies between billing and user modules.",
    "confidence": 0.78,
    "trace_id": "call_abc123",
}
```

The user-facing Python code usually receives the value:

```python
score: int = 64
```

The trace is recorded separately unless the caller asks for evidence in the return shape.

## Mocking and Tests

Tests should mock agent calls and verify deterministic orchestration.

```python
def test_setup_topic_team_blocks_when_agent_env_inputs_are_not_ready(fake_agent, tmp_path):
    fake_agent.when_do(
        "Resolve or create the registered Research Topic",
        returns=StageResult(status="ready", evidence=["topic ready"]),
    )
    fake_agent.when_invoke(
        "isomer-admin-topic-workspace-mgr",
        returns=StageResult(status="ready", evidence=["workspace ready"]),
    )
    fake_agent.when_invoke(
        "isomer-srv-topic-env-setup",
        returns=StageResult(status="ready", evidence=["topic env ready"]),
    )
    fake_agent.when_check(
        "Do the existing topic-team, workspace topology, and topic env evidence satisfy the prerequisites",
        returns=False,
    )

    result = setup_topic_team(tmp_path, "set up the team")

    assert result.status == "blocked"
```

This test does not prove the topic env evidence is actually good. It proves that, given agent outputs, deterministic Python orchestration takes the right branch.

## Related Work

This design is adjacent to typed LLM functions, structured-output frameworks, and AI programming languages, but it keeps a narrower purpose. Fructose wraps LLM calls as strongly typed Python functions and uses an `@ai` decorator, while its repository currently says maintenance is paused. Magentic uses decorators such as `@prompt` and `@chatprompt` to integrate LLM calls with typed Python functions. Marvin focuses on structured outputs and observable AI workflows. BAML treats prompts as functions, but uses an external language and generated clients. DSPy uses typed signatures, modules, and optimizers for AI programs. LMQL is a Python-superset language for constraint-guided LLM programming. Pydantic AI and Instructor show the broader ecosystem direction toward typed, validated structured outputs.

Agent-Primitive Python keeps the agent boundary explicit:

- Python remains Python.
- Agent calls are visible as `agent_*`.
- Cross-skill routes are visible as `agent_invoke`.
- Static checkers can inspect process shape without interpreting prose documents as code.

## References

- [Fructose](https://github.com/bananaml/fructose)
- [Magentic](https://github.com/jackmpcollins/magentic)
- [Marvin](https://pypi.org/project/marvin/)
- [BAML](https://github.com/boundaryml/baml)
- [DSPy](https://dspy.ai/)
- [LMQL](https://github.com/eth-sri/lmql)
- [Pydantic AI structured output](https://pydantic.dev/docs/ai/core-concepts/output/)
- [Instructor](https://python.useinstructor.com/)
- [Python ast](https://docs.python.org/3/library/ast.html)

## Open Questions

- Should Agent-Primitive Python remain documentation-only, or should Isomer add a validator that parses real Python skill-process files?
- Should `evidence=True` change the return type to `AgentAnswer[T]`, or should evidence always live in the runtime trace store?
- Should `agent_invoke` allow service-to-service repair calls in any future workflow, or should cross-skill orchestration stay operator-owned by default?
