# Historical NBA source lineage: metadata-only release

Historical audit conducted September 28, 2026. These metadata tables and SHA-256 references were recovered from `NBA_Historical_Source_Inventory.zip`; the original source files and URLs are documented without republishing the raw NBA injury-report PDF archive or third-party schedule PDFs/HTML.

## Files

- `NBA_Source_Inventory.csv`: 30 source records documenting release dates, URLs, verification and source/archive IDs.
- `injury_report_inventory.csv.gz`: 37,342 original injury-report URL checks. Only records where `pdf_present=True` indicate one of the 27,755 saved and individually hash-verified PDFs. Do not confuse checked URLs with acquired PDFs.
- `injury_archive_summary.csv`: seven physical injury-report archives, including the 2025–26 targeted archive. Not every season is a complete hour-by-hour source mirror; 2020–21 especially has fewer recovered reports.
- `primary_sample_report_map.csv.gz`: all 7,230 sampled games joined to selected official report URLs, SHA-256 and header timestamps; 2,054 unique saved PDF objects were selected.
- `archived_game_report_links.csv.gz`: 14,460 archived older/latest and cadence panel link records (with different game key conventions).
- `boxscore_source_map.csv.gz`: all 7,230 NBA game IDs and original raw JSON cache paths with **candidate** download endpoints, not proof of the endpoint that supplied each game.
- `selected_report_timestamp_exceptions.csv`: 21 affected game selections mapped to eight PDFs on December 19–21, 2025, where their printed header times are 15 minutes later than the filename/manifest timestamps. Every affected selected report is still pre-tipoff, but checkpoint eligibility warrants a fresh exact-clock re-selection.
- `ORIGINAL_SOURCE_MEMBER_SHA256.json`: checksums of the source archive's uncompressed metadata files, plus the original source ZIP's SHA-256.

## Verification

From repository root (Python standard library only):

```bash
python3 provenance/historical_sources/verify_source_and_coding.py
```

This checks metadata hash integrity, the 7 per-archive PDF counts, candidate and selected game counts, selected-report joins, the 21 timing exceptions, and the 300-row independent coder agreement statistic. It does **not** hash raw NBA PDFs, reconstruct injury-report parsing, or independently prove human independence.

## Important scope limitation

The complete 27,755 PDF archive and original 7,230 raw NBA boxscore JSON payloads are **not in this repository**. The historical source inventory identifies expected original ZIPs and paths, but the actual cached JSON payloads remain unverified/missing. The original collection timestamps were not preserved. Archive member hashes and recorded HTTP Last-Modified are not substitutes for original download times.

This source audit was conducted after the underlying regression datasets were frozen. The 21 header/manifest timestamp mismatches are disclosed but the report selection algorithm has not yet been rerun with corrected timestamps. Therefore these source metadata do not prove a complete raw-to-paper reproduction.

Broadcast: the current October manuscript treats the national-partner definition **including 2025–26 streaming-only games** as the primary exposure. The older historical inventory's use of the words 'legacy' or 'harmonized TV' describes source-building terminology and must not be used to relabel the October outcome specifications.
