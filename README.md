# NBA Player Participation Reforms and Star Availability

**Current analysis:** November 2026 cadence-harmonized panel with the star-definition correction (scientific-v2)
**Previous manuscript version:** October 25, 2026 (historical)
**Historical analysis freeze:** August 12, 2026
**Seasons:** 2020–21 through 2025–26 (regular season)

This repository examines changes in star-player absence onset, national-TV exposure, home/road absences, injury-report wording, and absence timing around the NBA's 2023 participation reforms. The Player Participation Policy, 65-game awards threshold, and NBA Cup began together; these observational comparisons **do not isolate the causal effect of the PPP** or establish that individual injury reports were misleading.

## Which October dataset version? Read this first

Three October cadence panels exist. They are different data versions, not competing reproductions of one result. Each has exactly one entry point.

| Version | What it is | Entry point | Decoded SHA-256 | Primary full-control estimate (N = 180,530) |
| --- | --- | --- | --- | --- |
| Frozen (Aug 12) | Historical reference. Published freeze; original chronology; contains the SCI-001 star error | `data_intermediate/player_team_game_harmonized_cadence.csv.gz` (no rebuild needed); models via `scripts/data_rebuild/replay_stage6_from_frozen.py` | `3c161f95…` | +2.630 pp, p = .046 |
| Legacy corrected chronology | Historical reference. Frozen builder plus the February 2022 Toronto chronology correction; **still contains the SCI-001 star error** | `scripts/data_rebuild/reproduce_final_datasets.py` (this section) | `2409b501…` | +2.674 pp, p = .043 |
| Scientific-v2 (SCI-001) | Legacy corrected chronology with the 49 report-only star flags corrected; **adopted primary** | `scripts/data_rebuild/reproduce_october_scientific_v2.py` ([setup and command](documentation/OCTOBER_SCIENTIFIC_V2_2026-11-15.md)) | `9dde4578…` | +3.064 pp, p = .019 |

The same SCI-001 correction applied to the *frozen* chronology gives +3.019 pp (p = .020); that is a diagnostic of the frozen phase, not a fourth release. August panels are not affected by SCI-001.

**Platform:** the historical Stage-6 estimator is validated only on Linux x86-64 with OpenBLAS (CI, or a `linux/amd64` container). On macOS arm64 its rank-deficient full-control covariance breaks down, so every Stage-6 caller now refuses unsupported platforms and rejects exploded standard errors. The explanation is in `scripts/data_rebuild/stage6_numerics.py`.

The October 25 manuscript reports the estimate from the frozen panel (the first row above) and is kept as a historical version. The November reconstruction, the star-definition correction and the reproducibility tooling are documented in the [November 2026 audit README](documentation/NOVEMBER_2026_AUDIT_README.md); the terms on which data are shared are in [DATA_STATEMENT.md](DATA_STATEMENT.md).

## Rebuild the legacy corrected datasets (historical pipeline, pre-SCI-001)

The one-command rebuild `scripts/data_rebuild/reproduce_final_datasets.py` deliberately reproduces the historical builders and keeps their strict hashes. Its October output is the legacy corrected-chronology panel (`2409b501…`), which still contains the star-definition error. Private-input requirements and commands are in [REPRODUCE_FINAL_DATASETS.md](documentation/REPRODUCE_FINAL_DATASETS.md). For the adopted scientific-v2 panel, use `scripts/data_rebuild/reproduce_october_scientific_v2.py` as described in [OCTOBER_SCIENTIFIC_V2_2026-11-15.md](documentation/OCTOBER_SCIENTIFIC_V2_2026-11-15.md).

## October 25, 2026 version (historical)

For the **October 25 manuscript**, use `manuscript/october_2026/`, the results in `results/october_2026/`, and the rerun scripts in `scripts/october_2026/`. Its headline onset triple difference is **+2.63 percentage points** (95% CI +0.05 to +5.22; p = 0.046; N = 180,530) using cadence-harmonized reports and advance national-partner TV **including streaming-only games**. Excluding the 2025–26 streaming-only national games gives **+1.24 pp** (95% CI −1.35 to +3.82; p = 0.347) on the same sample. Neither estimate is evidence of a uniquely identified PPP causal effect. The +2.63 pp finding is sensitive to the TV definition.

The **August 12 freeze is not replaced**. Original `results/FINAL_RESULTS_TABLE.csv`, `results/CORE_MANUSCRIPT_RESULTS.csv`, `packages/`, `data_final/` and root `MANIFEST_SHA256.csv` remain historical analysis artifacts; their original README is preserved as `documentation/AUGUST_2026_FREEZE_README.md`. In particular, the August +3.15 pp latest-pre-tip coefficient is **not** the October headline estimate.

## Documentation index

See **[Documentation version guide](documentation/README.md)** for the current October manuscript and results, verification evidence, and a clear distinction between the historical August freeze documents and later October research updates. The August freeze artifacts and root August SHA-256 manifest are preserved unchanged.

## October 2026 files

- `manuscript/october_2026/` — audited October 25 paper, LaTeX source, referenced figures, and identification audit.
- `results/october_2026/manuscript_estimates.csv`, `diagnostic_tests.csv`, `manuscript_sample_summary.json` — compact October manuscript summaries (added by the previous pull request).
- `results/october_2026/archive/` — **unaltered executed output CSVs** from `NBA_Reruns_Results_and_Code_2026-10-25.zip`.
- `results/october_2026/audit_archive/` — output tables from the October methodological audit scripts.
- `scripts/october_2026/` — corresponding archived Python scripts, with only path portability adjustments (and distinct output names for two event-window joint-test files).
- `documentation/OCTOBER_2026_REPRODUCIBILITY.md` — execution instructions, provenance, selection and measurement limitations.
- `manifests/OCTOBER_2026_SHA256.csv` — SHA-256 checksums of files added/updated in this release (separate from August's historical manifest).

## Reproduce the October analyses

Install dependencies from `requirements.txt` / `requirements-lock.txt` in a Python 3.12 environment. The October scripts need `numpy`, `pandas`, `scipy` and `statsmodels`. On a cloned repository:

```bash
python3 scripts/october_2026/verify_release.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_base.py
```

For every archived rerun, see `documentation/OCTOBER_2026_REPRODUCIBILITY.md`. Recomputed outputs are placed in `results/october_2026/recomputed/` and are ignored by Git. The archived reference tables remain immutable.

## Data and provenance scope

This is **analysis-ready reproducibility**, not a full raw NBA injury-report PDF / official box-score JSON mirror. The cadence-selected main input is `data_intermediate/player_team_game_harmonized_cadence.csv.gz` (248,778 player–team–games, 180,664 onset-risk observations, 12,731 onsets). `data_final/player_game_panel_analysis_ready.csv.gz` provides historical player-star classifications for an alternative All-Star-only analysis. The underlying input archives also appear in `packages/01_analysis_ready_panel.zip` and `packages/06_cadence_harmonized_identification.zip`.

The public injury-label analysis uses historical latest-pre-tip extraction rather than the main October cadence panel. The original September 2026 human-coder worksheets, manual and scoring script have now been recovered: see `validation/independent_human_coding_2026_09/`. Recomputed agreement is 260/300 (86.7%; Cohen's κ = 0.835); independence was researcher-confirmed and cannot be proved from worksheet bytes. See `documentation/SOURCE_AND_HUMAN_CODING_EXTENSION_2026-10-29.md`.

## Historical source inventory and coder evidence (October 29, 2026 extension)

The 7 historical injury-report archive indexes, 7,230-game selected-report map, boxscore-ID lineage, and **21 selected timestamp exceptions** are documented under `provenance/historical_sources/`. These are original source *metadata*, not a complete mirror of raw PDFs/JSON or a fresh raw-to-analysis rebuild.

The original coder sheets, protocol and reproduction script are under `validation/independent_human_coding_2026_09/`. Verify with `python3 provenance/historical_sources/verify_source_and_coding.py` (Python standard library only).

The October 25 pre-extension README and manifest are preserved under `documentation/previous_october_release/`, so earlier released documentation remains traceable.
