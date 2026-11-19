# October 25, 2026 reproducibility guide

## Source provenance

This release uses source files preserved in the user's October 25 research archives:

1. `NBA_Cadence_Harmonized_Reruns_2026-10-25.zip` — 8 executed analysis scripts, 31+ coefficient/result CSVs, original input ZIPs, source-run report and hash manifest.
2. `NBA_Reruns_Results_and_Code_2026-10-25.zip` — exact same scripts/results, without the large duplicate input ZIPs.
3. `NBA_Method_Audit_Reproducibility.zip` — later October 25 audited LaTeX manuscript and figures, 2 identification diagnostic scripts and their executed coefficient tables.

The archived scripts' computational logic was not modified. To run in the repository, absolute `/mnt/data/...` input/output paths were replaced by paths relative to this checkout. Both event-window scripts previously wrote `event_window_joint_tests.csv`; output names are distinct now to prevent overwriting. Archive outputs are preserved byte-for-byte in `results/october_2026/archive` and `audit_archive`.

## Inputs and matching checksums

| Repository input | SHA-256 | Bytes |
| --- | --- | ---: |
| `data_intermediate/player_team_game_harmonized_cadence.csv.gz` | `5483fc07465b84b20d29f54f0c49da53bef367cba712ad174111f3a7a794d8cd` | 18,277,761 |
| `packages/06_cadence_harmonized_identification.zip` | `821b50373d0ab6f27237d05f2d1d2b32f669f2ebbcd25e7fe0cdd5cd8292b221` | 18,614,042 |
| `packages/01_analysis_ready_panel.zip` | `a3d991bdaf41cbdba734abbd43853b495b27fbb96576743259413fcd50eb9155` | 28,085,705 |

The panel's *Git blob SHA-1* (not its SHA-256) is `d74c2b6ef473a564333933ffbf31c05afb68db9a`, which matches the file listing of the shared GitHub repository before this patch. Original source data are not modified.

## Run and verify

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/october_2026/verify_release.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_base.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_event.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_placebo.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_home.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_home_extra.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_timing.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_event_window_harmonized.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_event_window_legacy.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/audit_models.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/audit_cluster.py
```

The archive results live in `results/october_2026/archive/` and the audit archived results in `results/october_2026/audit_archive/`. Any new executions write into `results/october_2026/recomputed/`; the output is not meant to be committed automatically. Rerun baseline against the archived DDD coefficient tables; tolerances for numeric comparison should account for floating-point environments. A failure to reproduce the numeric result should be reported, not silently edited.

The 2025–26 streaming-only 101 games are included in `announced_tv_primary` (national partners) but excluded in `tv_harmonized_linear` (linear only). The prefix `legacy` in archived regression labels refers to a TV definition and does **not** mean latest-pre-tip reporting when the archived panel is cadence selected.

## Different estimands and limitations

- Main TV onset regression: 180,530 complete-case observations, from 180,664 cadence at-risk observations (248,778 panel rows; 12,731 new onsets).
- Home/road confirmed one-game and longer-spell regressions: 180,087 records, following-game censoring rule.
- Preperiod fake-date placebos: 87,788 records; event-time, hazard and short-spell analyses use different observed-risk sets.
- The historical latest-pre-tip 180,695 controlled model is **not** the current cadence model, despite some older root results labeling it the primary anchor.
- The August wording and taxonomy outputs use different report timing; do **not** describe them as October cadence-harmonized reruns.
- Reported 260/300 human-coder agreement and κ = 0.835 lack complete coder sheets in this release. They cannot be independently rechecked from this bundle.
- The 2023 PPP, 65-game eligibility threshold and NBA Cup coincide; results cannot isolate one reform's causal impact.
- Raw season-by-season injury-report PDFs and box-score JSON are not included here, and a September source audit identified 21 2025–26 selected-report timing/manifest discrepancies that warrant investigation before raw-PDF-to-final-panel reproduction is claimed.
- Some October exploratory event-window return tests have low unadjusted p-values under linear-TV-only; multiplicity and risk-set selection prevent a strong causal interpretation.

## Paper version

`manuscript/october_2026/` contains the method-audited October 25 version (a later same-day methodological revision), not the earlier October 25 un-audited version. The folder includes `main.tex`, two referenced PDF figures and the original audited manuscript PDF. Compile from inside that folder using a LaTeX distribution supporting the packages in `main.tex`.


## October 29 source/coding provenance extension
A later addendum at `documentation/SOURCE_AND_HUMAN_CODING_EXTENSION_2026-10-29.md` supplies the previously missing original coder worksheets and scoring script, plus independently checkable historical source metadata. The October 25 snapshot above retains its original historical context. Run `python3 provenance/historical_sources/verify_source_and_coding.py`. No original NBA PDF/JSON payloads were added or re-parsed as part of that extension.
