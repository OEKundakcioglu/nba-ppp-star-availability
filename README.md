# NBA Player Participation Reforms and Star Availability

**Current manuscript and analysis extension:** October 25, 2026
**Historical analysis freeze:** August 12, 2026
**Seasons:** 2020–21 through 2025–26 (regular season)

This repository examines changes in star-player absence onset, national-TV exposure, home/road absences, injury-report wording, and absence timing around the NBA's 2023 participation reforms. The Player Participation Policy, 65-game awards threshold, and NBA Cup began together; these observational comparisons **do not isolate the causal effect of the PPP** or establish that individual injury reports were misleading.

## Which version to use

For the **current October 25 manuscript**, use `manuscript/october_2026/`, the results in `results/october_2026/`, and the rerun scripts in `scripts/october_2026/`. Its headline onset triple difference is **+2.63 percentage points** (95% CI +0.05 to +5.22; p = 0.046; N = 180,530) using cadence-harmonized reports and advance national-partner TV **including streaming-only games**. Excluding the 2025–26 streaming-only national games gives **+1.24 pp** (95% CI −1.35 to +3.82; p = 0.347) on the same sample. Neither estimate is evidence of a uniquely identified PPP causal effect. The +2.63 pp finding is sensitive to the TV definition.

The **August 12 freeze is not replaced**. Original `results/FINAL_RESULTS_TABLE.csv`, `results/CORE_MANUSCRIPT_RESULTS.csv`, `packages/`, `data_final/` and root `MANIFEST_SHA256.csv` remain historical analysis artifacts; their original README is preserved as `documentation/AUGUST_2026_FREEZE_README.md`. In particular, the August +3.15 pp latest-pre-tip coefficient is **not** the October headline estimate.

## Current October files

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
