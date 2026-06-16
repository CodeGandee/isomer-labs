# Prepared Workspace Facts — DeepResearch (prepare-workspace, no launch)

Custom operator-owned, per-quest workspace (workspace.toml). Platform-level scaffolding created here;
per-quest roots + Experimenter git worktrees are materialized at quest-create / start (need a quest_id
and the quest's operator-owned repo at quest.workspace_ref).

## Paths
- LOOP_DIR:        /home/linfeng/houmao_DeepScientist
- HARNESS (abs):   /home/linfeng/houmao_DeepScientist/execplan/harness/bin/deepresearch    (also set as launch env HARNESS on all 6 profiles)
- STATE DB (abs):  /home/linfeng/houmao_DeepScientist/runs/state.sqlite         (initialized: schema + seed — 28 tables, 13 stages, 15 knowledge packs; 0 quests — no quest created/launched yet)
- shared (RO):     /home/linfeng/houmao_DeepScientist/shared/{objective,baseline}   (seeded by Orchestrator at scope/baseline, runtime)
- artifact_root:   /home/linfeng/houmao_DeepScientist/runs/<quest-id>/              (per quest, created at quest-create/start)
- work roots:      /home/linfeng/houmao_DeepScientist/runs/<quest-id>/workspaces/<role|instance-id>  (per quest/start)

## Deferred to start (not done here)
- (DONE) state init — the DB is initialized + seeded; quest creation/launch is still deferred
- per-quest runs/<quest-id>/ dirs + role work roots
- Experimenter git worktrees off quest.workspace_ref
- notifier-prompt attachment via houmao-agent-gateway
