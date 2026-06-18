# Project Goal

## Intent

Isomer Labs aims to become an interactive, semi-automatic research-conduction platform. A human user defines the Research Topic, supplies context, chooses constraints, and steers the work at critical decision points. Multi-agent research teams do the heavy research work between those points.

The platform should help a user move from a research question to useful artifacts: literature notes, hypotheses, baselines, experiment plans, implementation work, result analyses, reports, figures, and decision records. The system should not replace the researcher. It should make the research process more observable, easier to steer, and easier to reuse.

## Research Engine

The core engine is a multi-agent research team. Each team can include agents for roles such as scouting, planning, literature review, experiment design, coding, analysis, writing, critique, and decision support.

The user should be able to choose a Domain Agent Team Template based on the research methodology of a field, then specialize it into a Topic Agent Team Profile for the user's concrete research topic. Team openness is a core design goal, not an advanced-only feature. A research problem may need a narrow team of two agents, while a larger project may need a staged group with specialized reviewers and operators.

At the center of the engine is an operator agent controlled by the user. The operator agent coordinates team activity, asks the user for decisions, translates user intent into team instructions, and presents work products back to the user.

## Human Steering

The platform should treat human steering as part of the research loop.

The user should be able to:

- set the Research Topic and optional Measurable Objectives
- provide background materials, code, data, and constraints
- approve or redirect research plans
- choose among candidate ideas or experiment routes
- inspect intermediate artifacts before the system builds on them
- pause, relate, resume, or archive Research Inquiries and Research Topics
- override team composition and workflow structure when needed

The system should ask for human input at moments where autonomy is risky or preference-heavy, such as problem framing, baseline acceptance, experiment route selection, claim strength, and final recommendations.

## Relationship to DeepScientist

Isomer Labs is inspired by DeepScientist, which is available locally under `extern/orphan/DeepScientist`. DeepScientist demonstrates how a research system can organize work around durable skills, quest state, staged workflows, and research artifacts.

Isomer Labs should learn from that model, but it should differ in these design directions:

- Agent teamwork is a first-class design target.
- Users can use predefined Domain Agent Team Templates, specialize Topic Agent Team Profiles, or define their own agent-team structure.
- Team customization remains open and visible to the user.
- The system favors modular, white-box control over opaque automation.
- The research engine and GUI are decoupled.
- The operator agent mediates between the user and the research team.
- The GUI is generated for the specific research task and artifact set.
- Project state can live inside a user-owned project instead of a system-owned workspace.

## Modular, White-Box Platform

Isomer Labs should expose its structure clearly. Users should be able to inspect the active Research Topic, Research Inquiries, team roles, task plan, artifacts, decisions, prompts, tool calls, and research state. The platform should make it clear why a team is doing a task and what evidence supports each conclusion.

The project should avoid a single closed pipeline. Instead, it should define composable pieces:

- project state and artifact storage
- Domain Agent Team Templates and Topic Agent Team Profiles
- operator-agent control loop
- research workflow templates
- task-specific GUI generation
- external tool and codebase integrations
- evidence, decision, and provenance records

This modularity should let Isomer Labs integrate into a user's own repository or research workspace. The system should not require the user to move all work into a fully controlled platform directory.

## GUI Direction

The GUI should not be a fixed dashboard that tries to fit every research task. It should be generative and task-specific.

For each research project, the GUI should visualize the artifacts that matter for that task: papers, claims, experiment matrices, code changes, result tables, figures, decision points, open risks, and next actions. The research engine should be able to describe what needs to be visualized, while the GUI layer renders the right view for the current task.

The GUI remains separate from the research engine. The engine should be useful from command-line or agent workflows, and the GUI should act as an interactive visualization and steering layer.

## Desired Research Loop

```text
Research Topic and context
        |
        v
Operator agent clarifies topic and proposes Topic Agent Team Profile/workflow
        |
        v
User approves, edits, or replaces Topic Agent Team Profile/workflow
        |
        v
Research team executes visible, staged work
        |
        v
Artifacts, evidence, and decisions are recorded
        |
        v
Generated GUI visualizes task-specific state
        |
        v
User steers, branches, pauses, or continues
```

## Early Design Questions

- What is the smallest useful agent-team abstraction?
- How should users define custom agent teams without writing too much boilerplate?
- Which decisions must always return to the user?
- What project state belongs in Isomer Labs metadata, and what should remain in user-owned files?
- How should task-specific GUI generation describe views, data bindings, and user actions?
- How much DeepScientist workflow structure should Isomer Labs reuse, adapt, or replace?
- What artifact format best preserves evidence, provenance, and user decisions?
