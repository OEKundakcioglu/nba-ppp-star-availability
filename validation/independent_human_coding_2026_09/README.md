# Independent human coder archive — September 2026

The original `Encoded1.csv` and `Encoded2.txt` judgment files, locked coding manual, development reference, scoring script, pairwise comparison and disagreement list were recovered from `NBA_Coding_Agreement.zip`. They are retained byte-for-byte, without adjudicating disagreement or altering the frozen taxonomy.

From this folder, run `python3 score_supplied_codings.py`. It uses only the Python standard library and recomputes 260 agreements and 40 disagreements on 300 records, observed agreement 86.6667% and unweighted Cohen's kappa 0.8348813209494325. The reference sheet is assistant-coded and **not a medical gold standard**.

The package's provenance JSON records the researcher's September 27 confirmation that two humans classified independently, without viewing the reference or each other's labels. The data confirm ID/description consistency and agreement, but do not independently prove that independence or timing of the original coding exercise; coder names and completion dates were not supplied.

The coding sheet contains **publicly reported injury/reason designations of NBA players**, not confidential medical records. This is the *development* sample used to refine the taxonomy, not a held-out evaluation. The 40 original disagreements remain untouched. Avoid using this package as a new blinded handoff because it includes reference labels.
