# Prepared Workspace Facts — DeepResearch (prepare-workspace, no launch)

Custom operator-owned, per-quest workspace (workspace.toml). Platform-level scaffolding created here;
per-quest roots + Experimenter git worktrees are materialized at quest-create / start (need a quest_id
and the quest's operator-owned repo at quest.workspace_ref).

## Paths
- LOOP_DIR:        /home/linfeng/houmao_DeepScientist
- HARNESS (abs):   /home/linfeng/houmao_DeepScientist/execplan/harness/bin/deepresearch    (also set as launch env HARNESS on all 6 profiles)
- STATE DB (abs):  /home/linfeng/houmao_DeepScientist/runs/state.sqlite         (NOT initialized — deferred to the explicit start step)
- shared (RO):     /home/linfeng/houmao_DeepScientist/shared/{objective,baseline}   (seeded by Orchestrator at scope/baseline, runtime)
- artifact_root:   /home/linfeng/houmao_DeepScientist/runs/<quest-id>/              (per quest, created at quest-create/start)
- work roots:      /home/linfeng/houmao_DeepScientist/runs/<quest-id>/workspaces/<role|instance-id>  (per quest/start)

## Deferred to start (not done here)
- state init (/home/linfeng/houmao_DeepScientist/runs/state.sqlite) via `deepresearch state init`
- per-quest runs/<quest-id>/ dirs + role work roots
- Experimenter git worktrees off quest.workspace_ref
- notifier-prompt attachment via houmao-agent-gateway
