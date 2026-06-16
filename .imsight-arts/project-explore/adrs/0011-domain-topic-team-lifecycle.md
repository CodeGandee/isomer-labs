# Domain and Topic Agent Team Lifecycle

Isomer Labs will expose agent teams through three user-facing lifecycle terms: **Domain Agent Team Template**, **Topic Agent Team Profile**, and **Agent Team Instance**. A Domain Agent Team Template captures the research methodology of a research field, a Topic Agent Team Profile specializes that method for a user's research topic before anything is running, and an Agent Team Instance exists only after the profile is launched for execution.

## Status

accepted

## Considered Options

- Keep the prior two-step model: Agent Team Template directly becomes Agent Team Instance.
- Add a topic-level profile while keeping the shorter Agent Team Template name.
- Use the explicit domain/topic terms: Domain Agent Team Template, Topic Agent Team Profile, and Agent Team Instance.

## Consequences

- User-facing docs, GUI labels, schema fields, and manifest fields should expose the domain/topic distinction.
- The Operator Agent specializes Domain Agent Team Templates into Topic Agent Team Profiles before launching Agent Team Instances.
- **Agent Profile** remains the individual-agent construction/configuration term; avoid bare "Profile" when team-level and individual-agent concepts are both in scope.
