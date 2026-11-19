# Commit SHA map

On 2026-11-20 the commit history from `0a7f49d` onward was rewritten to correct commit author and message metadata. No file changed: each rewritten commit has the same tree as the commit it replaces.

Evidence documents and JSON files written before that date cite the earlier commit SHAs. The table below gives the current commit for every earlier SHA cited in this repository. The full map of all 334 rewritten commits is in [`validation/commit_sha_map_2026-11-20.csv`](../validation/commit_sha_map_2026-11-20.csv).

To check a pair, confirm that `git rev-parse <current commit>^{tree}` prints the tree SHA shown.

| Cited commit | Current commit | Tree | Cited in |
| --- | --- | --- | --- |
| `f4caffd55322` | `dfb227175055` | `c711bc9e84bc` | `documentation/AUTHENTIC_2020_OCTOBER_DOWNSTREAM_2026-11-14.md` |
| `dbd9603eba7a` | `f06641694f96` | `98e93b816c5c` | `documentation/AUTHENTIC_2021_OCTOBER_DOWNSTREAM_2026-11-14.md` |
| `a4a7ca3326b1` | `8e77f2e0f916` | `6d7d9d95e7cb` | `documentation/AUTHENTIC_2022_OCTOBER_DOWNSTREAM_2026-11-14.md` |
| `040b99cba8f8` | `59ece9182b1e` | `05e3fdc3917b` | `documentation/AUTHENTIC_2023_OCTOBER_DOWNSTREAM_2026-11-14.md` |
| `835a01609439` | `f3c264ca1058` | `5bd39d04d097` | `documentation/AUTHENTIC_2024_OCTOBER_DOWNSTREAM_2026-11-14.md` |
| `18abb2dda84f` | `5377810c1a22` | `ea1074a347cc` | `documentation/AUTHENTIC_RAW_JSON_FINAL_RUN_2026-11-13.md` |
| `ab45ad376d60` | `905f22d07b57` | `1e14745e9151` | `documentation/AUTHENTIC_RAW_JSON_FINAL_RUN_2026-11-13.md` |
| `2513c0e72c18` | `60550ef18837` | `1afe64f856e4` | `documentation/AUTHENTIC_SCI001_CORRECTED_BUILDER_2026-11-15.md`, `validation/october_scientific_v2_2026-11-15/authentic_primary_acceptance.json`, `validation/october_scientific_v2_2026-11-15/authentic_secondary_acceptance.json`, `validation/october_scientific_v2_2026-11-15/execution_closeout.json`, `validation/october_scientific_v2_2026-11-15/review_release_candidate.json` |
| `21b6f617f08d` | `ca9159c23bbf` | `0607761d77d4` | `documentation/AUTHENTIC_SCI001_CORRECTED_BUILDER_2026-11-15.md`, `validation/october_scientific_v2_2026-11-15/authentic_primary_acceptance.json`, `validation/october_scientific_v2_2026-11-15/execution_closeout.json` |
| `a4c7299e7ae2` | `f8125187236b` | `ee3302cf72e3` | `documentation/AUTHENTIC_SELECTOR_JSON_FINAL_RUN_2026-11-14.md` |
| `70ebe218ceac` | `772040f3c33c` | `28b74ecd6d79` | `documentation/CONTROLLED_2025_TEAM_METADATA_EXPERIMENT.md`, `scripts/data_rebuild/experiment_2025_team_metadata.py` |
| `c0ce14f2765f` | `49ea38d69af0` | `96e1f038ed60` | `documentation/FINAL_REPRODUCIBILITY_RELEASE_REVIEW_2026-11-15.md`, `validation/final_release_audit_2026-11-15/audit.json` |
| `ddef0b805bc3` | `a780e233743b` | `5803eda3dd78` | `documentation/FINAL_REPRODUCIBILITY_RELEASE_REVIEW_2026-11-15.md`, `documentation/SIX_SEASON_CONNECTED_REPRODUCTION.md`, `validation/final_release_audit_2026-11-15/audit.json`, `validation/six_season_cumulative_2026-11-15/cumulative_acceptance.json`, `validation/six_season_end_to_end_2026-11-15/verification.json` |
| `dbc12ddf6f51` | `c49aeb733074` | `55b77a90bed7` | `documentation/OCTOBER_SCIENTIFIC_V2_2026-11-15.md`, `validation/october_scientific_v2_2026-11-15/implementation_and_availability.json` |
| `334277e5675a` | `1ef747c90977` | `133efbeb6716` | `documentation/PRIVATE_SOURCE_RECOVERY_AUDIT_2026-11-09.md`, `documentation/REPRODUCIBILITY_COMPLETION_REPORT_2026-11-09.md` |
| `0a7f49dc040f` | `8c70b5e9beca` | `28490521d19d` | `documentation/REPRODUCIBILITY_COMPLETION_REPORT_2026-11-09.md` |
| `7ac75bdf4c60` | `94c8b4409469` | `bf32d3d0387f` | `documentation/REPRODUCIBILITY_COMPLETION_REPORT_2026-11-09.md` |
| `db06d466fa0b` | `f32a8ab917bc` | `ae2eee12d803` | `documentation/SCI001_MANUSCRIPT_REVIEW_CANDIDATE_2026-11-15.md`, `validation/october_scientific_v2_2026-11-15/review_release_candidate.json` |
| `31fcef0d32bf` | `d79b070ebd56` | `25c9615c863b` | `documentation/SCIENTIFIC_INTEGRITY_AUDIT_2026-11-15.md`, `validation/scientific_integrity_audit_2026-11-15/findings.json`, `validation/scientific_integrity_audit_2026-11-15/review_scope.json` |
| `de8827c86271` | `403bcdc7cee9` | `dce73a629499` | `validation/october_scientific_v2_2026-11-15/authenticated_calendar_check.json`, `validation/october_scientific_v2_2026-11-15/implementation_and_availability.json` |
| `7ea2474518c7` | `a172fcdd8b00` | `2de9c53eeda8` | `validation/october_scientific_v2_2026-11-15/execution_closeout.json`, `validation/october_scientific_v2_2026-11-15/review_release_candidate.json` |
