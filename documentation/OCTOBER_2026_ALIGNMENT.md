# October 25, 2026 manuscript alignment

This is an **additive manuscript-alignment patch**. It retains the historical August 12 freeze unchanged and does **not** claim to re-execute models. Results are transcribed from the October 25 final manuscript and the October 25 robustness rerun report; the two baseline DDD values were cross-checked against `results/CORE_MANUSCRIPT_RESULTS.csv` already in the shared repository.

## Paper-aligned specification

- **Main**: 2020-21 to 2025-26, cadence-harmonized injury-report timing, national-partner advance TV **including streaming-only coverage**: DDD +2.63 pp (95% CI 0.05 to 5.22), p=0.046, N=180,530.
- **Mandatory TV sensitivity**: same selected-report cadence and sample, linear-TV-only exposure excluding streaming-only Peacock and Prime games: +1.24 pp (95% CI -1.35 to 3.82), p=0.347, N=180,530.
- Earlier **latest-pre-tip** estimates (+3.15 pp and +1.77 pp) are August historical specifications; do not call them the October headline result.
- Full cadence-harmonized panel: 248,778 player-team-games; 180,664 at-risk; 12,731 onsets. The N=180,530 estimate is the complete-cases controlled model and is **not** the whole at-risk set.
- Main outcome remains **new absence onset**, not prevalence; changes in risk set and player composition affect interpretation.

## Source reports

- `NBA_Player_Participation_Final_2026-10-25.tex` (October manuscript in the project file library)
- `NBA_Robustness_Rerun_Report.md` (October 25 rerun); this patch contains its reported summaries, not its executable code or full coefficient tables
- `NBA_Identification_Audit.pdf` (October 25 diagnostics)
- `NBA_Historical_Source_Audit.md` (September 28 historical source inventory)

## Methodological distinctions

- The 2023 PPP, 65-game awards threshold, and In-Season Tournament began together. Findings are observational and cannot identify the separate causal effect of PPP.
- The August conditional vague-versus-specific mechanism models use latest-pre-tip reports, not the October cadence-harmonized primary risk set. Keep their provenance explicit and do not relabel as rerun.
- The original August taxonomy QA describes a single assistant coder. The October manuscript separately reports two independent human coders, 260/300 agreement (86.7%, kappa 0.835). Do not overwrite the original QA or imply the raw coder sheets were verified by this patch.
- Joint pretrend p=0.616 and preperiod placebo p=0.511 / 0.867 belong to the October cadence-harmonized rerun, whereas older p=0.433 / 0.247 / 0.932 belong to August latest-pre-tip analysis.
- Home/road one-game interaction: +1.41 pp, p=0.093, N=180,087. One-/longer-spell analyses exclude onsets without observed follow-up; do not equate their N with the TV model's N.
- 2025-26 uses streaming-only national-partner coverage and different TV selection. The +2.63 pp result is borderline and sensitive to the TV definition.

## What is not yet done

- No raw PDFs, boxscore JSON, source schedule CSVs, or August frozen model outputs were edited.
- No new harmonized panel bytes, executed October scripts, full coefficient exports, or new raw-source hash verification are bundled. Locate the **October rerun archive** and add its actual scripts, inputs, and full result files before claiming complete October reproducibility.
- There is a documented December 2025 PDF-header/manifest timing discrepancy affecting 21 selected games; check exact-clock cadence if re-executing source selection.
- The original root `MANIFEST_SHA256.csv` remains **the August 12 freeze manifest**, not a manifest of this October extension.
