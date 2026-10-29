# NBA PPP paper — cadence-harmonized robustness replication

**Date:** 25 October 2026
**Source:** Frozen six-season public NBA player-game panel (2020–21 to 2025–26) and archive of the common-report-time reconstruction.
**Status:** New regressions were actually executed using the archived panel and code. This is a supplementary verification exercise, not a rewrite of the manuscript.

## 1. Regression baseline and star-definition sensitivity

| Estimand | Estimated DDD, 95% CI, p, N |
|---|---|
| Harmonized linear-TV primary | +1.24 pp [-1.35, +3.82], p=0.347, N=180,530 |
| Legacy national-TV | +2.63 pp [+0.05, +5.21], p=0.046, N=180,530 |
| All-Star-only, harmonized TV | +1.61 pp [-0.94, +4.16], p=0.216, N=180,530 |
| All-Star-only, legacy TV | +2.99 pp [+0.43, +5.54], p=0.022, N=180,530 |

The baseline figures reproduce the manuscript's cadence-harmonized coefficients (approximately +1.24 and +2.63 percentage points). For the All-Star-only rerun, the historical star indicators were taken from the archived latest-pre-tip panel and linked by identical player-team-game keys; 60 new harmonized records without identical keys inherited within-player-season classifications or original PPP status where unobserved. The cadence at-risk sample includes additional previously non-risk observations, so the archived number of 38 altered at-risk rows need not equal the new at-risk difference.

## 2. Pre-period event study and placebo reform dates

| Check | Recomputed result |
|---|---|
| Joint equality of pretrend interaction contrasts; harmonized TV | Wald χ²(2)=0.970, p=0.616, N=180,530 |
| Same, legacy TV | Wald χ²(2)=0.969, p=0.616, N=180,530 |
| Fake start 2021–22 (preperiod only) | +1.27 pp [-2.52, +5.06], p=0.511, N=87,788 |
| Fake start 2022–23 (preperiod only) | -0.31 pp [-3.97, +3.34], p=0.867, N=87,788 |

TV definitions coincide during the actual preperiod, so the fake-date results are identical under both labels. These tests do not reject the relevant null hypotheses; they do not establish the counterfactual parallel-trends assumption. The original archived p values (joint pretrend 0.433, fake dates 0.247 and 0.932) were **not** the cadence-harmonized reruns.

## 3. Home / road and spell-duration checks

| Check | Recomputed result |
|---|---|
| Exactly one-game onset, Star × Post × Home | +1.41 pp [-0.24, +3.05], p=0.093, N=180,087 |
| At least two games, placebo | -0.26 pp [-1.67, +1.15], p=0.719, N=180,087 |
| All-Star-only star definition | +1.41 pp [-0.23, +3.05], p=0.093, N=180,087 |
| Exclude NBA Cup | +1.34 pp [-0.31, +2.98], p=0.111, N=175,015 |
| Exclude 2020–21 and 2021–22 | +3.12 pp [+0.73, +5.50], p=0.010, N=123,176 |

These use player, team-season, and *physical game* fixed effects; standard errors are clustered by player and physical game. One-game and >=2-game episodes are established only when the following team game is actually observed. Rows with an onset lacking a consecutive follow-up are excluded from these outcomes. This conservative censoring rule yields N=180,087 for the main home/road comparison rather than the N=180,320 in the latest-pre-tip archive. The pandemic-excluded model has only one pre-reform season; do not promote it to a new headline estimate.

## 4. Short-spell and repair-hazard timing

| Check | Recomputed result |
|---|---|
| One-game spell immediately before linear-TV | +0.06 pp [-1.97, +2.09], p=0.954, N=178,080 |
| Spell <=2 games, TV within next 2 team games | -0.74 pp [-2.41, +0.92], p=0.380, N=175,739 |
| One-game spell immediately before legacy-TV | -0.02 pp [-2.01, +1.96], p=0.982, N=178,080 |
| Spell <=2 games, legacy-TV within next 2 games | -0.37 pp [-2.13, +1.39], p=0.682, N=175,739 |
| Repair hazard, linear-TV | +4.95 pp [-1.65, +11.56], p=0.142, N=50,370 |
| Repair hazard, legacy-TV | +5.08 pp [-1.16, +11.33], p=0.111, N=50,370 |

The return model uses only continuing spells with a documented onset and controls flexibly for games elapsed within the spell. This is **not guaranteed to be numerically identical** to the older repair sample/age-control implementation; the model is explicitly defined in the attached script.

### ±3-game event-window joint tests (relative to anchor game)

| Outcome | Harmonized TV p | Legacy TV p |
|---|---:|---:|
| New absence onset | 0.804 | 0.744 |
| Absence prevalence | 0.725 | 0.712 |
| Return to availability | **0.0158** | 0.0563 |

The event-time construction assigns each team game to a *uniquely* nearest announced TV game within ±3 team games, discarding equidistant ties. The models use player and team-season fixed effects, full schedule controls, and player/game clustering. The return model controls flexible absence age. The return interaction is joint-significant under linear-TV coding but not the legacy definition at 5%; the notably negative relative +3-event coefficient in the linear model is around −16.77 percentage points (unadjusted p=.0082). Treat this as sensitive, exploratory event-time heterogeneity and consider adjustment for multiple outcomes and windows; it is not evidence of a causal PPP response.

## 5. Interpretation and limitations

1. The main harmonized-TV coefficient remains imprecise; none of these reruns establishes the PPP's causal effect separate from other 2023 participation reforms.
2. Home/road effects, placebo spells, and short-spell timing are directionally similar or remain nonsignificant. Some original effect estimates differ because the construction and fixed-effect specifications changed.
3. This artifact reruns the formerly archived checks on the cadence-harmonized **analysis panel**. It does not reconstruct the NBA injury-report PDFs and box scores from their raw origin, nor validate the underlying injury descriptions against confidential medical records.
4. Event-time return observations condition on prior absence and therefore remain subject to risk-set composition/selection effects. Results should be described as associations.
5. The primary report-cadence and TV-definitions themselves are not causally randomized, and season-dependent national-TV selection remains a concern.

## 6. Files and reproducibility

The package includes two original compressed input archives (`inputs/`), the actually executed Python regression scripts (`scripts/`), and complete coefficient tables plus compact summary results (`results/`). No older regression outputs have been substituted for the new ones. The scripts were split into independent batches to make rerunning large fixed-effect models practical.

All software dependencies: Python 3, pandas, NumPy, SciPy, statsmodels. BLAS threads may be capped to two for repeatable runtimes. Paths in the provided scripts assume source archives have been extracted under `/mnt/data/nba_work/` (see `README.md`). Inference uses normal-approximation two-sided p values with two-way clustered covariance (and chi-squared Wald joint tests).
