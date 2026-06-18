# action: datastmt (nature-data → Data-Availability statement)
`$HARNESS --via skill:deepresearch-manuscript-aux/datastmt:<role> manuscript datastmt --quest-id <q> \
  --artifact-id <q>:datastmt --ref runs/<q>/report/data-availability.md --input <inventory.json>`
Drafts only from the verified data inventory; never invents DOIs/accessions; avoids "available on request".
