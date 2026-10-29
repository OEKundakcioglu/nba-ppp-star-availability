# December 2025 PDF report-clock exceptions: exclusion sensitivity

**Audit executed:** October 29, 2026. **Data vintage:** cadence-harmonized October 25, 2026 analysis panel. This audit is deliberately **additive**; it does not change the October 25 manuscript, its original panel, results, or any August historical data.

## What happened

The historical source inventory compared the manifest timestamp to the printed header timestamp on each saved NBA injury-report PDF. Among the 7,230 selected regular-season game reports, 21 games between **December 19–21, 2025** use eight saved PDF objects with header times **15 minutes later** than the manifest/filename times.

All 21 are still **strictly before tip-off** by the header time. Their corrected pre-tip lead times range from **15 to 195 minutes**. In particular, the Toronto Raptors at Brooklyn Nets and Miami Heat at New York Knicks selections for December 21 have **15 minutes of lead** rather than the previously recorded 30. Although there is no demonstrated post-tip information leakage, the selected reports do not occur at exactly the nominal 1:30/5:30/8:30 ET checkpoint on these eight PDFs. No claim is made that an exact-clock re-selector would choose the same PDF for every game.

These 21 games cover **733 player–team–game panel observations**, of which **514 were in the onset-risk set**, including **35 recorded onsets**. Those are already-coded observations, not recodings from corrected PDFs.

## Fitted exclusion sensitivity

The original October model with player and team-season fixed effects, the complete published pregame controls, and two-way clustering by player and physical game was rerun **unchanged**, first on the entire October cadence panel and then dropping the 21 affected games from the already constructed at-risk sample. No report was reselected or re-parsed, and features for subsequent games were not reconstructed.

| TV definition | Sample | DDD estimate (pp) | 95% CI (pp) | p | N |
|---|---|---:|---|---:|---:|
| National-partner including streaming | Full | +2.6304 | [+0.0458, +5.2151] | 0.0461 | 180,530 |
| National-partner including streaming | Exclude 21 games | +2.6295 | [+0.0410, +5.2180] | 0.0465 | 180,016 |
| Linear-TV-only | Full | +1.2390 | [-1.3457, +3.8236] | 0.3475 | 180,530 |
| Linear-TV-only | Exclude 21 games | +1.2538 | [-1.3240, +3.8316] | 0.3404 | 180,016 |

**Interpretation:** The estimates and inference change very little when the entire set of exception games is excluded. This is reassuring with respect to their sample influence **but does not resolve selection/extraction at the correct clock time**. The +2.63 pp national-partner estimate remains near the conventional 0.05 threshold and does not establish a PPP causal effect.

## Reproduce

From the repository root with packages `numpy`, `pandas`, `scipy`, and `statsmodels` installed:

```bash
python3 scripts/october_2026/verify_timestamp_exception_sensitivity.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python3 scripts/october_2026/run_timestamp_exception_sensitivity.py
```

The first command checks hashes and archived coefficient values without refitting. The second fits four models using the original October model logic and saves recomputed output in the ignored `results/october_2026/recomputed/timestamp_audit/` folder. It compares the DDD and sample counts against the committed four-row reference file. Environment-dependent numerical differences should be examined rather than silently patched.

## Provenance and limitations

- `results/october_2026/timestamp_audit/selected_report_clock_audit.csv` joins the independently archived source inventory to the original selected game map; exact game IDs, source URLs, hashes and both reported times are retained.
- `results/october_2026/timestamp_audit/model_sensitivity.csv` contains the newly executed complete model's key DDD coefficients.
- `results/october_2026/timestamp_audit/analysis_scope.json` records the sample and scope.
- Source metadata from `provenance/historical_sources/` were verified against original archive manifests in the preceding audit, but this run did **not** reopen or hash the raw PDF bytes.
- Dropping games after already defining absence-onset risk and pregame controls is a robustness check. A **proper corrected-clock full reconstruction** would reselect snapshots using genuine PDF header publication times, reparse the selected report contents, reconstruct at-risk spells/lagged covariates for affected and downstream games, then rerun all outputs. The raw season PDF source archives and raw box-score JSON remain outside the GitHub repository.
- No evidence from this audit proves that either of the two PDFs at 15 minutes before tip contains information inaccessible earlier; it simply identifies the timing discrepancy.

## Suggested wording for manuscript / response to reviewers

> A source-provenance audit identified 21 games assigned to eight injury-report PDFs whose printed issue time was 15 minutes later than the manifest time. All remained pre-tip, but two selected game reports had only 15 minutes' actual lead. Excluding all 21 games from the analysis-ready risk set left the headline national-partner triple-difference estimate essentially unchanged (2.630 to 2.630 percentage points, with p = 0.0461 versus 0.0465); this is an influence sensitivity, not a replacement for a corrected-clock report-selection exercise.
