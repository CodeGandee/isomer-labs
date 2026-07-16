The Kimi agent did not choose exports/kaoju-paper itself. It invoked export-template without --target, so isomer-cli selected its
  hardcoded managed default:

  <topic-workspace>/exports/kaoju-paper/<paper-line>/vNNNN

  That default is implemented in src/isomer_labs/kaoju/paper.py:214. The isomer-2 pane and the corresponding /home/huangzhe/.kimi-code/
  sessions/wd_isomer-labs_e39046c41ca0/session_c10cd257-fec5-4a54-8773-dd3823815bdd/agents/main/wire.jsonl show that the agent omitted
  --target.

  The current design distinguishes these locations:

  Canonical MyST template
      records/artifacts/...                         canonical managed state
          |
          +-- export-template
                exports/kaoju-paper/.../vNNNN      actor-editable exchange copy

  intent/derived/...                               derived intent and environment specifications

  The Kaoju skill explicitly treats manual template access as an export. src/isomer_labs/assets/system_skills/research-paradigm/kaoju/
  isomer-kaoju-pipeline/commands/create-paper-template.md:9 says the export is versioned and derived, but is not canonical state. src/
  isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-kaoju-pipeline/commands/manage-paper-template.md:5 then tells the agent
  to use the actor target or managed default.

  Your expectation of intent/derived comes from the earlier Kaoju design. The archived specification placed a canonical LaTeX template at
  intent/derived/writing-template/<template-name>/. That requirement was later explicitly superseded by the MyST-first design, as
  recorded in src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-kaoju-pipeline/resources/survey-process.v2.json:72.

---

our intended protocol is:
- `intent/derived/writing-template/<template-name>/` is the for exporting a MyST template so that user can edit it and then re-import it into the Kaoju pipeline. The exported template is not canonical state; it is a user-editable copy.
- `.../writing-template/main/` is the MyST template that is considered as the currently used template for the Kaoju pipeline, if user does not name the template explicitly, it is where exports go by default.
- `isomer-cli` should be able to list the named templates in db, and user can say "update <template-name> based on <exported-template-path>" to update the template in db, export to merge with the current template works similarly. The exported template is not canonical state; it is a user-editable copy.
- if user says "update the paper template in db", "update the currently used paper template", or something that means updating the template inside the current artifacts db, without naming the template, specifying the template path, or specifying the export path, then the Kaoju agent should discover the target template in this order:
    1. is it an exported template previously exported by the user, and then edited? If so, use that.
    2. do we have `.../writing-template/main/` in the current topic dir? If so, use that.
    3. if neither of the above, this is a confusing situation, and the Kaoju agent should ask the user to clarify which template to use.
- template update is agentic work because we simply have no standard format of paper template, `isomer-cli` will not be able to take a template dir and update the template in db without the help of agent.
- `isomer-cli` can be used for CRUD operations on the template in db, but keep the api to low level editing (like, editing the myst template inside db, or some json metadata, etc), and let the agent handle the high level logic of template construction, there is no way to convert an arbitrary user-edited template into a canonical template without the agent's help, as we do not restrict the user to a specific template schema. The principle is, we still want to avoid agent directly doing the template editing via SQL update, but we do not want to force a schema on the user either.
- we do not want to complicate template revision management with versioning like git, just
    - allow agent to use `isomer-cli` to update an existing template in db
    - templates are named and can be listed in db, revision can be created explicitly by user or agent, like a snapshot
    - support replacing the template in db with a known snapshot, but complicated merging should be done by agent, who constructing a new template from the snapshot and the current template in db, and then update the template in db with the new one.
    - `template snapshot` is not a separate concept, it is just another named template in db, agent may choose specific naming convention to indicate that it is a snapshot.
