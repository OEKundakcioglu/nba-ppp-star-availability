# Independent NBA injury-label coding manual — locked v1

## Goal
Independently classify the **initial official designation text** for each sampled absence spell. Do not infer whether an injury is genuine, strategic, exaggerated, or "fake." This exercise measures reproducibility of the wording taxonomy only.

## What to code
Use only `initial_designation_raw` in the blinded sheet. Ignore any outside knowledge about the player, team, season, injury history, game importance, or how long the absence lasted. If the designation is blank/unusable, code `unknown`.

Enter exactly one of these six labels in `coder_2_class`:

- `explicit_rest` — the substantive designation explicitly says rest/resting (including rest with an added contextual phrase). Use this before any other category.
- `illness` — illness, COVID/non-COVID illness, health-and-safety protocol language, or another clearly illness-related designation.
- `other_non_injury` — a non-medical absence reason such as personal reasons, suspension, G League assignment/two-way status, not-with-team status, trade/transaction status, or return-to-competition/reconditioning language that is presented as a non-injury reason.
- `specific` — a concrete diagnosis/pathology or clearly diagnostic medical term. Examples include sprain, strain, fracture, contusion, tear, surgery/post-surgical status, tendinopathy/tendinitis, inflammation, bursitis, concussion/concussion protocol, hyperextension, abrasion, and meniscectomy. A body part by itself is not enough. If both a specific term and vague/management language appear, code `specific`.
- `vague` — medical wording that identifies discomfort/management without a concrete diagnosis. Examples include soreness, tightness, stiffness, swelling, irritation, spasms, effusion, injury management, injury recovery, and generic "injury" wording without a concrete diagnosis.
- `unknown` — blank, missing, unusable, or genuinely impossible to classify from the text alone.

## Precedence rule
If more than one category appears to apply, use this order:

`explicit_rest` > `illness` > `other_non_injury` > `specific` > `vague` > `unknown`

The generic header `Injury/Illness -` is **not itself evidence of illness**. Classify the substantive text that follows it.

## Coding procedure
1. Read one row at a time.
2. Assign one exact label from the six allowed values.
3. Use `coder_2_notes` only when the row is ambiguous or you want to record why you chose a label.
4. Do not consult another coder or the project’s existing labels while coding.
5. Do not change `coding_id` or `initial_designation_raw`.
6. Complete all 300 rows before discussing disagreements with the researcher.

This manual is frozen before coder 2 begins. Any later adjudication rule changes must be documented separately and must not overwrite the original coder-2 responses.
