#!/usr/bin/env python3
"""regression suite — default participant roster includes the BO-reviewer (7th, default-launched).

The BO-reviewer is NOT an optional add-on: every quest prepares and launches it like the other roles. These
checks pin the SOURCE-OF-TRUTH roster so a future edit cannot silently drop it back to a 6-agent default:

  - specs/state/seed.toml          role roster lists BO-reviewer (tool=codex product default)
  - agents/bindings.toml           a [[bindings]] for BO-reviewer exists
  - specs/collab/topology/...      a bo-review route to BO-reviewer exists
  - manifest.toml [participants]    agents includes BO-reviewer AND total_live_instances_default == 7
  - agents/bo-reviewer.toml         product default backend=codex / effort=max (the durable default)
  - the persistent claude-fallback mechanism is a documented local-override FILE PATH (gitignored)

Run:  python3 tests/binding/test_roster.py   (exits non-zero on any failure)
"""
import sys, json, pathlib, tomllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PASSED, FAILED = [], []


def check(label, cond, detail=""):
    (PASSED if cond else FAILED).append(label)
    print(("  PASS " if cond else "  FAIL ") + label + (("  -- " + detail) if detail and not cond else ""))


def load(rel):
    return tomllib.load(open(ROOT / rel, "rb"))


def main():
    # R1: seed role roster includes BO-reviewer with the codex product default
    print("R1 seed.toml role roster includes BO-reviewer (codex product default):")
    seed = load("execplan/specs/state/seed.toml")
    roles = {r["instance_id"]: r for r in seed.get("role", [])}
    bo = roles.get("BO-reviewer", {})
    check("R1: BO-reviewer is a seeded role with tool=codex; full default roster is the 7 expected ids",
          bo.get("tool") == "codex"
          and set(roles) == {"orchestrator", "scout-ideator", "experimenter", "analyst", "writer",
                             "reviewer", "BO-reviewer"},
          "roles=%s bo=%s" % (sorted(roles), bo.get("tool")))

    # R2: bindings.toml has a BO-reviewer binding
    print("R2 bindings.toml binds BO-reviewer:")
    binds = load("execplan/agents/bindings.toml").get("bindings", [])
    parts = {b["participant"] for b in binds}
    bob = next((b for b in binds if b["participant"] == "BO-reviewer"), {})
    check("R2: a BO-reviewer [[bindings]] exists (tool=codex product default, instance BO-reviewer)",
          "BO-reviewer" in parts and bob.get("tool") == "codex"
          and bob.get("instances") == ["BO-reviewer"], "parts=%s" % sorted(parts))

    # R3: topology has the bo-review route to the BO-reviewer
    print("R3 topology routes bo-review to BO-reviewer:")
    topo = load("execplan/specs/collab/topology/topology.toml")
    routes = topo.get("route", [])
    bo_route = next((r for r in routes if r.get("to") == "BO-reviewer"), {})
    check("R3: a route to BO-reviewer carries the bo-review stage",
          bo_route.get("from") == "orchestrator" and "bo-review" in (bo_route.get("stages") or []),
          "route=%s" % bo_route)

    # R4: manifest participants list + default-live count are 7 (BO-reviewer included)
    print("R4 manifest.toml default roster is 7 incl. BO-reviewer:")
    man = load("execplan/manifest.toml")
    pa = man.get("participants", {})
    check("R4: [participants].agents includes BO-reviewer AND total_live_instances_default == 7",
          "BO-reviewer" in (pa.get("agents") or []) and pa.get("total_live_instances_default") == 7,
          "agents=%s total=%s" % (pa.get("agents"), pa.get("total_live_instances_default")))

    # R5: durable product default is codex / max (never silently rewritten by a machine-local override)
    print("R5 bo-reviewer.toml product default is codex / max:")
    rv = load("execplan/agents/bo-reviewer.toml").get("reviewer", {})
    check("R5: product default backend=codex, effort=max", rv.get("backend") == "codex" and rv.get("effort") == "max",
          "backend=%s effort=%s" % (rv.get("backend"), rv.get("effort")))

    # R6: the claude-fallback persistence mechanism is a documented, gitignored local-override FILE.
    print("R6 claude-fallback local-override path is documented + gitignored:")
    gi = (ROOT / ".gitignore").read_text()
    check("R6: execplan/agents/bo-reviewer.local.toml is referenced in .gitignore (machine-local fallback file)",
          "bo-reviewer.local.toml" in gi, "gitignore has no bo-reviewer.local.toml entry")

    # R7: the record + comms schemas must ALLOW BO-reviewer (else participant.register / bo-review dispatch
    # silently fail — the exact gap that would block default-launching the role).
    print("R7 participant + task-request schemas allow BO-reviewer:")
    prole = json.load(open(ROOT / "execplan/specs/state/records/participant.schema.json"))["properties"]["role"]["enum"]
    treq = json.load(open(ROOT / "execplan/specs/comms/schemas/task-request.schema.json"))
    # to_role enum lives under the nested payload object; find it structurally.
    found = "BO-reviewer" in json.dumps(treq)
    check("R7: participant.role enum AND task-request to_role enum both include BO-reviewer",
          "BO-reviewer" in prole and found, "participant_roles=%s task_request_has_bo=%s" % (prole, found))

    # R8: a workspace policy exists for BO-reviewer (its binding references workspace.BO-reviewer).
    print("R8 workspace.toml defines a BO-reviewer policy:")
    wsa = {a["id"] for a in load("execplan/specs/workspace/workspace.toml").get("agent", [])}
    check("R8: workspace.toml has an [[agent]] id=BO-reviewer", "BO-reviewer" in wsa, "ids=%s" % sorted(wsa))

    print("\n%d passed, %d failed" % (len(PASSED), len(FAILED)))
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
