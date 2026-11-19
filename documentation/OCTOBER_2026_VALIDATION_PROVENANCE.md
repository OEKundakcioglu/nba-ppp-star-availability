# October human-coding validation: provenance and missing artifacts

The October 25 method-audited manuscript reports that **two independent human coders** reviewed the same 300 descriptions without seeing the AI reference labels or each other's labels. They agreed on **260/300 (86.7%)**, with **Cohen's κ = 0.835**.

These figures are **reported in the manuscript**, not independently reconstructed here. This repository's August `data_final/qa_summary.json` records an earlier assistant-based scoring stage and should **not** be rewritten to present the October human exercise as if the original August evaluation used two people. The per-coder raw labels, selection protocol and discrepancy adjudication files were not located in the October rerun archives used for this patch. If these exist, they need to be linked/published (subject to any privacy/permission considerations), with their own separate checksum and protocol.

Related caveat: taxonomy and public-injury-wording analyses retain latest-pre-tip extraction and do not share the main October cadence-harmonized report-timing sample. Injury specificity cannot confirm whether a report was genuine or deliberately misleading.


## October 29 provenance extension
The previously missing original `Encoded1.csv` and `Encoded2.txt` were located in the project library along with `NBA_Coding_Agreement.zip` (September 27, 2026). This release adds the original two worksheets, development sample reference, locked manual, scoring code and all disagreements at `validation/independent_human_coding_2026_09/`. An independent local execution of the original scoring script reproduced 260/300 agreement and Cohen's κ = 0.8348813209494325. See `documentation/SOURCE_AND_HUMAN_CODING_EXTENSION_2026-10-29.md`. The prior text above describes the *October 25 version before these files were found*; the worksheets are no longer missing.
