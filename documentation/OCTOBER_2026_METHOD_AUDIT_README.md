# NBA Participation Reforms: methodological review (25 October 2026)

## Contents

- `NBA_Identification_Audit.pdf`: independent methodological review, including estimands, model sensitivities and remaining identification limits.
- `Load_Management_Method_Audited.pdf`: 25-page updated manuscript with review-driven clarifications and an added identification-diagnostics appendix.
- `latex/main.tex`: editable LaTeX manuscript, with the two required original figure PDFs.
- `analysis/data/player_team_game_harmonized_cadence.csv.gz`: frozen source panel from the October 2026 archival rerun package, included for portable reproduction.
- `analysis/audit_models.py`: six regression diagnostics using fixed effects and two-way clustered uncertainty.
- `analysis/audit_cluster.py`: sensitivity to player/team-season clustering.
- `analysis/results/`: numeric results actually produced by the two scripts.

## Reproduce

Install Python pandas, numpy, scipy, statsmodels, and a LaTeX distribution with pdfLaTeX.

From `analysis/` run:

```
OPENBLAS_NUM_THREADS=2 python audit_models.py
OPENBLAS_NUM_THREADS=2 python audit_cluster.py
```

By default they read from `analysis/data/` and write to `analysis/results/`. The optional `NBA_AUDIT_PANEL` environment variable can override the dataset path.

To compile the paper, change into `latex/` and run `pdflatex main.tex` twice. The memo source is not part of the source package; the PDF is fully included.

## Scope

New checks: alternate control sets; fixed-effects-only estimation; player/team-season clustering; absence-prevalence as a distinct outcome; same-star cohort prevalence; review of censored spell lengths. Original national TV, home/road, timing and wording estimates were retained from the established manuscript and previously archived reruns, not newly re-estimated as part of this audit.

This audit **does not identify** an effect of the Player Participation Policy distinct from the simultaneous 65-game award rule and NBA Cup. Wording changes are not a medical audit. Reported p values are descriptive sensitivity results, not newly preregistered confirmatory tests.
