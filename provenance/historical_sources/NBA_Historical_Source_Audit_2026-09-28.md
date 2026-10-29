# Historical data-source inventory

The uploaded copies of the `nba-load-audit` season folders already preserve substantial source documentation. The earlier reference-audit note overstated the gap: the main task was to consolidate existing records, not reconstruct all sources from scratch.

## What was verified

- **27,755 saved injury-report PDFs** across six seasons, including the separate 2025–26 targeted archive. Every PDF's newly calculated SHA-256 matches its original manifest; no mismatches or missing files among records marked available were found.
- **All 7,230 games in the current primary cadence selector** link to saved PDFs and original NBA report URLs. These selections use 2,054 distinct PDFs.
- The five **2021–22 through 2025–26 broadcast schedule PDFs** are byte-identical to freshly downloaded official NBA files. Release dates and direct URLs are in `NBA_Source_Inventory.csv`.
- Six archived **2020–21 ESPN/ABC, TNT and NBA TV announcement pages** retain canonical URLs and publication dates, covering the two schedule releases. The NBA TV second-half page remains incomplete; this is already an exposure-coverage limitation in the paper.
- The box-score output preserves official NBA game IDs and original cache paths for **all 7,230 games**. The collection script preserves the NBA MediaOps and NBA CDN endpoint templates.
- All six original `nba-2020-UTC.csv` through `nba-2025-UTC.csv` schedule inputs were recovered and hashed. Their schema and filenames match Fixture Download; the provider attribution is recorded as an inference because an original download log was not preserved and current direct CSV requests returned HTTP 403.

## Injury archives by season

| Season | Saved PDFs | Coverage of saved files | Hash matches |
|---|---:|---|---:|
| 2020-21 | 617 | 2020-12-21 to 2021-07-20 | 617 |
| 2021-22 | 5,567 | 2021-10-19 to 2022-06-16 | 5,567 |
| 2022-23 | 5,541 | 2022-10-18 to 2023-06-12 | 5,541 |
| 2023-24 | 5,441 | 2023-10-24 to 2024-06-17 | 5,441 |
| 2024-25 | 5,566 | 2024-10-22 to 2025-06-22 | 5,566 |
| 2025-26 | 5,023 | 2025-10-21 to 2026-04-12 | 5,023 |

Counts describe saved source files, not the number of games, onsets, or PDFs selected for analysis. Earlier-season archives extend into the postseason. The 2025–26 total comprises 1,497 original hourly-filename PDFs plus 3,526 targeted quarter-hour PDFs; the latter is not a complete all-day archive.

## Broadcast source dates and links

| Season | Release | Official schedule PDF |
|---|---|---|
| 2020–21 | December 4, 2020 and February 24, 2021 | Separate ESPN/ABC and TNT announcement tables; exact links and saved HTML are in the inventory. |
| 2021-22 | [2021-08-20](https://pr.nba.com/2021-22-nba-schedule-75th-anniversary-season/) | [Verified PDF](https://pr.nba.com/wp-content/uploads/sites/46/2021/08/2021-22-NBA-Schedule-By-Date.pdf) |
| 2022-23 | [2022-08-17](https://pr.nba.com/2022-23-nba-schedule/) | [Verified PDF](https://pr.nba.com/wp-content/uploads/sites/46/2022/08/2022-23-NBA-Schedule-By-Date-8-17-22.pdf) |
| 2023-24 | [2023-08-17](https://pr.nba.com/2023-24-nba-regular-season-schedule/) | [Verified PDF](https://ak-static.cms.nba.com/wp-content/uploads/sites/46/2023/08/2023-24-NBA-Schedule-By-Date-as-of-8-17-23.pdf) |
| 2024-25 | [2024-08-15](https://pr.nba.com/2024-25-nba-regular-season-schedule/) | [Verified PDF](https://pr.nba.com/wp-content/uploads/sites/46/2024/08/2024-25-NBA-Regular-Season-Schedule-By-Date.pdf) |
| 2025-26 | [2025-08-14](https://pr.nba.com/2025-26-nba-regular-season-schedule/) | [Verified PDF](https://pr.nba.com/wp-content/uploads/sites/46/2025/08/2025-26-NBA-Regular-Season-Schedule-By-Date-8-14-25.pdf) |

The older TV package calls its variable `announced_tv_primary`; that historical label refers to what the current paper calls **legacy**. This inventory does not restore legacy as the primary specification. The current harmonized TV definition still excludes streaming-only coverage.

## Timing exceptions found during source verification

The inventory retains both the original manifest timestamp and the timestamp printed inside each PDF. **70 of 27,755 files differ**: four in 2020–21, one in 2021–22, and 65 in 2025–26. The first five are not selected by the primary cadence map. The 65 later files have printed times 15 minutes later than their manifest times.

Of those 65 files, **eight PDFs are selected for 21 primary-sample games on December 19–21, 2025**. Every selected PDF is still earlier than tip-off using its printed time. This does not establish an after-tip information leak, but it means those records' reported checkpoint times are 15 minutes too early relative to the PDF headers. The affected game/file pairs and actual lead times are isolated in `selected_report_timestamp_exceptions.csv`.

No model input, estimate, or paper text was changed during this source-inventory task. An exact-clock cadence analysis should review these 21 selections before claiming that every selected report has the stated checkpoint time. This audit alone cannot establish whether a re-selection would change any estimate.

PDF-header times are interpreted in America/New_York and converted to UTC. The one repeated-hour DST case uses the default first occurrence; it is outside the selected primary sample. Header time, server Last-Modified time, and download time are distinct fields. Original collection timestamps remain **unrecorded**; a ZIP modification time is not substituted for an access date.

One old 2020–21 audit README reports 5,088 “verified” PDFs. That is the number of candidate URL checks, including unsuccessful requests; the manifest and archive contain **617 successful PDFs**. This inventory corrects the source-file count without changing the manuscript's game counts.

## What remains missing

1. **Raw box-score JSON cache.** The compact uploaded output excludes the original payloads. It records relative locations under `nba_boxscore_roster_frame_v1_output/raw_json/`. Those files are needed to hash-check the box-score payloads and preserve them with the replication package. The per-game endpoint actually used cannot be established from the empty repair download log; both script endpoints are labeled candidates.
2. **Original acquisition timestamps.** Injury-report manifests preserve HTTP Last-Modified and ETag values, but no absolute request/download timestamp. The broadcast and schedule inputs also lack original acquisition logs. Preserve this limitation explicitly rather than treating current verification dates as original dates.
3. **Schedule-provider provenance.** The six original fixture CSVs and the transformation code are saved, but their original download log is absent. The visible Fixture Download format and link pattern support the provider attribution, not an independently verified byte match to a current download.
4. **Other covariate inputs.** The covariates package documents an internally reconstructed Elo measure and a static venue coordinate/time-zone table. The inventory covers the requested injury, schedule, box-score and broadcast inputs; it is not a complete external-source audit of award histories or each venue coordinate.

## Files and interpretation

- `NBA_Source_Inventory.csv`: compact, source-level inventory with URLs, archived filenames, dates, hashes, and verification status.
- `injury_report_inventory.csv`: all 37,342 original URL checks, including unsuccessful candidates; `pdf_present` identifies the 27,755 verified saved PDFs. Failed URL checks must not be counted as reports.
- `injury_archive_summary.csv`: per-archive counts, hash checks, date coverage and archive hashes.
- `primary_sample_report_map.csv`: all 7,230 current primary-sample game selections linked to exact report URLs and hashes.
- `archived_game_report_links.csv`: latest-pre-tip and archived common-time game-to-report links (14,460 rows).
- `selected_report_timestamp_exceptions.csv`: the 21 selected games with manifest/header time differences.
- `boxscore_source_map.csv`: official game IDs, anonymized relative cache paths and explicitly qualified endpoint candidates.
- `broadcast_sources/`: the eleven original broadcast-source files supplied in the existing TV package.
- `fixture_sources/`: the six original season CSVs.
- `evidence/`: original injury manifests, archive summaries, recovery checks, and relevant collection/transformation code. Personal home-directory prefixes were removed from the exported box-score map.

## Suggested manuscript source note

“Public injury reports are archived individually with their NBA source URLs, file hashes and report timestamps. The accompanying source inventory links each of the 7,230 games in the primary cadence sample to its selected report. Advance national-broadcast exposure is reconstructed from the two 2020–21 network schedule releases and the NBA's season-opening schedule PDFs for 2021–22 through 2025–26. The replication inventory distinguishes source publication times from original download times, which were not consistently recorded.”

The source note can be incorporated after the timestamp exceptions have been reviewed. It does not replace the missing raw box-score cache or establish a collection date that was never logged.
