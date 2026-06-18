# action: polish (nature-polishing → venue English polishing)
`$HARNESS --via skill:deepresearch-manuscript-aux/polish:<role> manuscript polish --quest-id <q> \
  --artifact-id <q>:polished --ref runs/<q>/report/paper-polished.md --input runs/<q>/report/paper.md`
Style only; flags overclaim terms as suggestions; never strengthens or adds claims.
