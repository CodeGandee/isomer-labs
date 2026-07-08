# Install System Skills

Isomer ships system skills that teach agents how to use the project, topic, operator, and DeepSci workflows. Install skills with `npx skills add` so your agent runtime can load them directly.

Install the operator entrypoint first:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint --agent codex --yes
```

Install the welcome skill when the agent should guide initial project setup:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/operator/isomer-op-welcome --agent codex --yes
```

Install the DeepSci pipeline skill when a research topic uses that extension:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/research-paradigm/deepsci/isomer-deepsci-pipeline --agent codex --yes
```

Use [Packaged System Skills](../developer/packaged-system-skills.md) when maintaining the skill source layout.
