# Wording taxonomy: supplied coding results

The two supplied files agree on **260 of 300 descriptions (86.7%)**, with unweighted **Cohen's kappa = 0.834881**, reported as **0.835**. There are 40 disagreements. The user confirmed on 27 September 2026 that the files were independently coded by two humans, without AI-generated classifications or access to each other's labels or the reference labels.

## File and sample checks

- `Encoded1.csv`: 300 distinct spell IDs, all labels present in `human_class_coder_1`.
- `Encoded2.txt`: comma-separated data, 300 distinct spell IDs, all labels present in `human_class_coder_2`.
- Both files match the original 300-spell development sample exactly by spell ID and description.
- All labels belong to the six permitted categories. No labels were corrected or adjudicated.

Expected agreement from the two coders' marginal distributions is 0.1925. Thus kappa = (260/300 − 0.1925)/(1 − 0.1925) = 0.8348813209494325.

## Disagreements

| Coder 1 | Coder 2 | Descriptions |
|---|---|---:|
| illness | vague | 20 |
| illness | other_non_injury | 11 |
| illness | specific | 8 |
| other_non_injury | explicit_rest | 1 |
| **Total** | | **40** |

The 11 illness/non-injury disagreements concern “Health and Safety Protocols.” The locked manual places this wording in illness. The 20 illness/vague disagreements include injury management, recovery, soreness, and inflammation. The eight illness/specific disagreements include concrete injury diagnoses and procedures. The last disagreement is “Rest - Trade Transition”; the manual gives explicit rest precedence. Inflammation is classified as specific in the locked manual, but coder 1 labels its three occurrences illness and coder 2 labels them vague. These patterns warrant discussion with the coders. Retain the original judgments and the agreement statistic before any adjudication.

## Comparisons with the archived development reference

| Comparison | Agreement | Cohen's kappa |
|---|---:|---:|
| Supplied coder 1 vs. supplied coder 2 | 260/300 (86.7%) | 0.835 |
| Supplied coder 1 vs. archived reference | 271/300 (90.3%) | 0.880 |
| Supplied coder 2 vs. archived reference | 286/300 (95.3%) | 0.941 |

The archived reference was assistant-coded. Its agreement with either supplied file is not agreement between two human coders and is not accuracy against a gold standard. Agreement between the two supplied files is the human inter-rater statistic reported in the manuscript.

## Manuscript update

> A vague description does not imply a false injury: minor and chronic conditions often lack a precise public diagnosis. The full panel is classified using a fixed keyword dictionary and precedence rules, refined using an AI assistant's coding of a 300-spell development sample. Two human coders independently classified the same 300 descriptions, without AI-generated classifications or access to each other's labels or the reference labels. They agreed on 260 descriptions (86.7%; Cohen's κ = 0.835). The 40 disagreements mainly concerned distinctions between illness, injury wording, and non-injury absences; the original judgments were retained when calculating agreement. This exercise measures inter-rater consistency on the development sample, not performance on held-out data. The coding measures the specificity of public wording, not medical truth.

The paper now reports the completed independent human coding. The full-panel taxonomy, wording regression, tables, and other estimates are unchanged. The 40 disagreements remain unaltered in the archived coding files. This is development-sample reliability, not held-out validation or a medical-truth assessment.

## Reproduction

The accompanying ZIP contains the two untouched supplied files, the matched archived reference, locked coding manual, scoring script, full comparison, 40-row disagreement list, confusion matrix, and machine-readable results. Run `python3 score_supplied_codings.py` inside the extracted folder. This is a researcher review package: it contains reference labels and must not be used as a blinded coding handoff.
