# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:FINALIZE-CONTEXT-BRIEF | SUMMARY.md, status.md, decisions, baselines, runs, analyses, writing outputs, review state | Closure context for the Research Topic or Inquiry. | isomer-rsch-finalize | closure gate | evidence |
| DEEPSCI:CLAIM-LEDGER | final claim ledger or equivalent summary | Claim status, evidence, caveats, and safe-surface decision. | isomer-rsch-finalize | final summary, writing, archive | report |
| DEEPSCI:FINAL-LIMITATIONS-REPORT | limitations and failure section | Final limitations, failures, deferred risks, and unsupported outcomes. | isomer-rsch-finalize | final summary and user | report |
| DEEPSCI:FINAL-SUMMARY | refreshed SUMMARY.md, final report artifact | Responsible final or pause-state summary. | isomer-rsch-finalize | user and future work | report |
| DEEPSCI:RESUME-PACKET | resume-packet-template output | Clean continuation path when later work is plausible. | isomer-rsch-finalize | future work | handoff |
| DEEPSCI:CLOSURE-DECISION | stop, park, publish, archive, route back | Durable closure or route-back decision. | isomer-rsch-finalize or decision | user and future work | decision |
| DEEPSCI:FINALIZE-BLOCKER-RECORD | failed closure gate | Why finalization is not responsible yet. | isomer-rsch-finalize | decision or upstream skill | decision |
| DEEPSCI:FINALIZE-CONTINUITY-UPDATE | status, summary, memory, graph, or route updates | Continuity record after finalization. | isomer-rsch-finalize | future work | runtime state |
