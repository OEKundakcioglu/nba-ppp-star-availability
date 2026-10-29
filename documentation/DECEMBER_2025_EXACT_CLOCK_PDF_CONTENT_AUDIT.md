# December 2025 exact-clock PDF content audit (29 October 2026)

## Question and scope

A previously merged source audit identified 21 games, December 19–21, 2025, assigned eight report PDFs whose **printed issue timestamps** were 15 minutes later than the selected nominal timestamp (`published_timestamp_utc` in the frozen selector). This bounded audit directly inspects the historical PDF bytes and tests whether substituting the latest archived PDF with printed issue time **at or before the original nominal cutoff** changes the October onset analysis.

The original August and October datasets, archived regression outputs and October 25 paper were **not modified**. This audit is additive.

## Evidence actually verified

- The uploaded `audit_2025_26_upload(1).zip` (SHA-256: `a0cdcb4b9e594a1b1fb63489aa43087f6c13f5b34ab3661b596c2941089c9f70`) holds all **16** relevant PDF objects: eight original selected PDFs and eight preceding candidates. All 16 independently recomputed PDF SHA-256 values match the historical source inventory and the accompanying candidate map.
- The first-page printed report header of each PDF matches the expected timestamp (checked after converting to America/New_York). In each affected game, the later report is issued **15 minutes after** its recorded nominal cutoff. Its eligible predecessor is issued **45 minutes before** that cutoff, as recorded in the preserved source inventory.
- For all 21 games, the candidate is the **latest available archived, hash-matched 2025–26 PDF with printed issue time no later than the cutoff**. This was checked across original and targeted source inventories, not merely between two filenames.
- Exactly **241 player entries** in the 21 selected game reports were linked one-to-one to the October analysis-ready panel using game, team and normalized player identity. All 241 selected PDF statuses **and reason strings** match the frozen panel. The earlier PDFs list the **same 241 players** for these games.
- Comparing earlier versus later PDFs shows **15 changed statuses involving nine games**, plus **one changed reason string** (Doug McDermott: earlier left-knee soreness; later `-`). See `results/october_2026/timestamp_audit/exact_clock/observed_report_changes.csv` and the 21-game summary.
- The October deterministic outcome formula was independently reapplied to all **733 player-game records** in these 21 games using the frozen box-score fields (`played_bool`, `boxscore_player_status`, `not_playing_reason`) and the archived report designation. All **733 of 733** original `absence_now_harm` values were reproduced. Substituting the corrected report statuses produces **zero changes** in the absence flag. The 21-game subset retains **514 onset-risk records and 35 absence onsets**.
- The report-player sets do not change, and the report-status coverage for the two snapshots is unchanged. Because none of the underlying absence flags change, the sequence-derived onset/risk flags and the published regression input variables are unchanged by *these specific 21 report substitutions*. Thus the previously published October headline coefficients do **not need numerical adjustment for this bounded correction**, subject to the exact measurement and selection rules stated here. This is not a claim of fresh re-estimation of every model.

## Method details

The historical report selector assigned a nominal report timestamp at the intended cadence checkpoint. The audited PDFs show that, on these three dates, the relevant PDF's issue time was 15 minutes after that nominal time. We compare the archived snapshot with the latest indexed predecessor already issued at that nominal cutoff. This changes the *reported status at the cutoff*, but in all 15 affected cases it does not change the absence outcome given the independent official box-score fields and the study's deterministic absence definition. For instance, an earlier `Doubtful` designation still yields an injury absence for Jaylen Brown because the box score records `DND_INJURY`.

The only changed reason text concerns Doug McDermott, who is not marked as an absence under the frozen outcome rule. The October headline regression does not use reason-text categories as covariates; historical injury-wording analyses use a different latest-pre-tip extraction, and this test does not recompute those analyses.

## How to reproduce

Obtain the original `audit_2025_26_upload.zip` (the uploaded copy here had the suffix `(1)`), but **do not add the raw PDF ZIP to Git**. From a checkout with `main` updated and the audit files installed:

```bash
python3 -m pip install pandas pymupdf
python3 scripts/october_2026/verify_exact_clock_pdf_review.py \
  --pdf-zip "$HOME/Downloads/audit_2025_26_upload(1).zip"
```

The verifier reads the original PDFs **in memory**; checks all 16 hashes and report titles; checks that the candidate is the latest eligible report in the historical inventory; validates every selected PDF player record against the original analysis panel; and reconstructs the recorded absence outcome before/after designation substitution from original box-score fields. It is read-only and does not overwrite any archived data.

## Limits: what this does NOT establish

1. The printed header and archived `Last-Modified` records are evidence of report timing but **not original acquisition/download logs**. This audit does not independently prove what a particular investigator could download at every historical instant.
2. The check repairs **only the 21 previously identified timing exceptions** in the analysis of the selected PDF. It is not an independent full-season sweep of every unrecorded report-timing ambiguity.
3. We have **not re-run the entire raw NBA PDF + boxscore JSON + roster identity + schedule reconstruction pipeline**. The bounded result depends on the existing validated panel identities, box-score fields, team report availability flags, and October model specification.
4. The study's observational identification limitations, sensitivity to TV definition and the absence of original raw boxscore JSON from the public repository remain unchanged.
5. The full PDF archive is **not republished** in this audit patch; only the reproducible code, source hashes, case metadata and change summaries are committed.

**Conclusion:** These 21 timestamp exceptions require source-provenance annotation. Within the exact frozen October model construction, using the earlier eligible report statuses changes zero absence outcomes or new-absence onsets. The October results should remain versioned and unaltered; this bounded proof should be disclosed rather than described as full raw-data replication.
