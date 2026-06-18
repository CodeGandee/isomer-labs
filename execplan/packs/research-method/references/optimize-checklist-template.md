# OPTIMIZE_CHECKLIST.md

- [ ] Read the durable frontier summary — in Houmao: `$HARNESS state query frontier` + `$HARNESS bo status` (`artifact.get_optimization_frontier(...)`)
- [ ] Select the primary optimize submode: `brief`, `rank`, `seed`, `loop`, `fusion`, or `debug`
- [ ] Confirm whether the current pass is `explore`, `exploit`, `fusion`, `debug`, or `stop`
- [ ] Review recent optimization memory before generating new candidates
- [ ] Check whether the current brief slate covers more than one mechanism family
- [ ] Candidate briefs updated or confirmed
- [ ] Candidate ranking updated
- [ ] Promote only the strongest brief(s) into durable line(s) if justified
- [ ] Current implementation candidate pool recorded
- [ ] Smoke queue defined
- [ ] Full-eval queue defined
- [ ] Recent failures classified and either debugged or archived
- [ ] Stagnation check performed
- [ ] Family-shift trigger checked
- [ ] Fusion eligibility checked
- [ ] Next concrete action written
