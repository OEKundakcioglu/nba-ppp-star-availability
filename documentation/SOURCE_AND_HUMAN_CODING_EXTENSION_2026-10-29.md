# October 29, 2026 — source-lineage and human-coding extension

This is a **provenance extension** to the merged October 25 analysis-ready reproducibility release. It adds no new regressions, no changed manuscript estimates, and no edits to the frozen August datasets or older raw-source objects. The original Oct 25 README, validation note, reproducibility note and SHA-256 manifest are preserved under `documentation/previous_october_release/` before the live documentation pointers are updated.

## What was newly recovered and checked

1. Historical source metadata from `NBA_Historical_Source_Inventory.zip`, with 37,342 injury-report URL checks, 27,755 successfully archived PDFs, 7,230 game-to-selected-PDF matches, and 7,230 box-score game IDs. This release ships *metadata* and original source file digests; it does not ship or rehash the PDFs or raw boxscore JSONs.
2. The complete `NBA_Coding_Agreement.zip` package: original human coder sheets (`Encoded1.csv` and `Encoded2.txt`), the locked coding manual, disagreement cases, reference and scoring script. Independently running that script reproduced 260/300 = 86.7% agreement and Cohen's κ = 0.834881.
3. The 21 selected game-to-report cases whose PDF header time was 15 minutes later than its manifest/filename time. All eight selected PDFs remain pre-tipoff, but an **exact-clock re-selection has not been executed**.

## Verification

```bash
python3 scripts/october_2026/verify_release.py
python3 provenance/historical_sources/verify_source_and_coding.py
```

The older October release checker verifies the **then-current README and October archive** via the updated README checksum in `manifests/OCTOBER_2026_SHA256.csv`; the exact manifest and README bytes from before this extension are preserved under `documentation/previous_october_release/`.

## Still open

- Recover and independently SHA-256-check the actual raw injury-report PDF archives and original boxscore JSON cache; the source metadata alone are insufficient.
- Review 21 exact-clock cadence report selections before claiming final report-time eligibility is fully independently verified.
- For independent full-panel rebuilding, document and replay the historical parsing, merging, classifier and schedule construction stages from source artifacts; source metadata are not a parser execution.
- Treat the reported coder independence as researcher-confirmed rather than separately observable from CSV data. This is development-sample inter-rater reliability, not held-out predictive validity.
