# Research repository documentation — version guide

**Index updated:** October 29, 2026

**Current manuscript:** October 25, 2026 (method-audited version)

**Historical analysis freeze:** August 12, 2026 (with an August 13 README clarification)

This page identifies the **current** results and verification records without modifying any historical August analysis files. Older documents remain accessible as versioned evidence, not as current instructions for quoting the October manuscript.

## Current manuscript and numerical results

| Purpose | Authoritative current artifact |
| --- | --- |
| Paper | [`manuscript/october_2026/`](../manuscript/october_2026/) — audited PDF, `main.tex`, and figures |
| Headline DDD | [`results/october_2026/manuscript_estimates.csv`](../results/october_2026/manuscript_estimates.csv) |
| Pretrend and placebo diagnostics | [`results/october_2026/diagnostic_tests.csv`](../results/october_2026/diagnostic_tests.csv) |
| Archived executed coefficients | [`results/october_2026/archive/`](../results/october_2026/archive/) and [`audit_archive/`](../results/october_2026/audit_archive/) |
| Executable October code | [`scripts/october_2026/`](../scripts/october_2026/) |
| Methodology and rerun instructions | [`OCTOBER_2026_REPRODUCIBILITY.md`](OCTOBER_2026_REPRODUCIBILITY.md) |

The **October main** estimate is **+2.63 percentage points** (95% CI +0.05 to +5.22; p = 0.046; N = 180,530) for cadence-harmonized injury reports and advance national-partner television **including streaming-only games**. The **linear-TV-only sensitivity** is **+1.24 percentage points** (95% CI −1.35 to +3.82; p = 0.347; N = 180,530). These observational differences do **not** separately identify the causal impact of the Player Participation Policy, the concurrent 65-game awards rule, or the NBA Cup. The main finding is sensitive to the TV definition.

## Later verification and source provenance

| Topic | Current evidence and qualification |
| --- | --- |
| Human-coder agreement | [`validation/independent_human_coding_2026_09/`](../validation/independent_human_coding_2026_09/) includes original worksheets and scoring code: 260/300 agreement (86.7%), Cohen's κ = 0.835. Researcher-confirmed independence cannot be independently established from files; this is *development-sample* inter-rater agreement, not held-out accuracy. |
| Historical report and box-score lineage | [`provenance/historical_sources/`](../provenance/historical_sources/) inventories 27,755 saved PDF objects and maps 7,230 games; those counts are metadata-supported. Raw source PDF bytes and original box-score JSON files are **not mirrored** in Git. |
| Timing exception influence | [`OCTOBER_2026_TIMESTAMP_EXCEPTION_SENSITIVITY.md`](OCTOBER_2026_TIMESTAMP_EXCEPTION_SENSITIVITY.md) — exclusion of 21 affected games barely changes the headline estimate; exclusion is not PDF re-selection. |
| Checked PDF content substitutions | [`DECEMBER_2025_EXACT_CLOCK_PDF_CONTENT_AUDIT.md`](DECEMBER_2025_EXACT_CLOCK_PDF_CONTENT_AUDIT.md) — 16 archived PDFs verified against original hashes; 21 affected games; 15 status changes; zero changes in reconstructed absence flags on 733 affected player-game observations. **Bounded check only**, not a full raw-to-paper rebuild. |
| Updated provenance chronology | [`SOURCE_AND_HUMAN_CODING_EXTENSION_2026-10-29.md`](SOURCE_AND_HUMAN_CODING_EXTENSION_2026-10-29.md) |

## Historical documents — retained unchanged

**The following pre-October files describe the August research freeze. Their estimates, sample definitions, and unfinished-task descriptions must not be mistaken for current October claims.** They have *not* been overwritten by this documentation-index update.

- [`AUGUST_2026_FREEZE_README.md`](AUGUST_2026_FREEZE_README.md): the August 13 clarified README retained as an historical release artifact. The August 12 original README bytes are represented in the historical root manifest, not in the current root README.
- [`FROZEN_SPECIFICATION.md`](FROZEN_SPECIFICATION.md) and [`MANUSCRIPT_READY_RESULTS.md`](MANUSCRIPT_READY_RESULTS.md): the historical latest-pre-tip analysis and its **+3.15 pp** headline. They do not describe the October headline specification.
- [`CLAIMS_AND_LIMITATIONS.md`](CLAIMS_AND_LIMITATIONS.md): August-era interpretation and taxonomy-validation wording. Its caution against claiming *independent human double-coding* was correct for that earlier stage; it has been superseded by the September human-coded worksheet evidence above.
- [`TAXONOMY_VALIDATION_PROVENANCE.md`](TAXONOMY_VALIDATION_PROVENANCE.md): documents an earlier assistant/Claude coding exercise, **not** the separately documented human-coding exercise.
- [`OPEN_ITEMS.md`](OPEN_ITEMS.md): August-era research to-do list. Its human-coding item is now addressed by the later worksheets, although independent process verification remains outside the archive.
- [`RAW_DATA_AND_REPRODUCIBILITY_SCOPE.md`](RAW_DATA_AND_REPRODUCIBILITY_SCOPE.md) and [`RELIABILITY_STAGE10_RESULTS.md`](RELIABILITY_STAGE10_RESULTS.md): original freeze-stage source and reliability context.
- [`OCTOBER_2026_ALIGNMENT.md`](OCTOBER_2026_ALIGNMENT.md): describes the *initial* summary-only October patch. Its contemporary statement that scripts were not yet bundled is no longer true for the current merged repository; see the rerun guide above.

## Integrity checks and what they establish

Run from the repository root in a Python environment with the stated requirements installed:

```bash
python3 scripts/october_2026/verify_release.py
python3 provenance/historical_sources/verify_source_and_coding.py
python3 scripts/october_2026/verify_timestamp_exception_sensitivity.py
```

The first and third commands inspect hashes, sample counts and **archived** coefficients; neither is a fresh regression run. A full October baseline rerun is separately available through `scripts/october_2026/run_base.py` (see the reproducibility guide). The content-level PDF audit also needs the **separately retained original** `audit_2025_26_upload.zip`:

```bash
python3 scripts/october_2026/verify_exact_clock_pdf_review.py --pdf-zip /path/to/audit_2025_26_upload.zip
```

Keep raw PDFs outside Git. Original raw box-score JSON payloads and collection logs are not fully available in this public repository; therefore the archive is **analysis-ready reproducibility**, not an end-to-end independent raw-source reconstruction.

## Versioned manifests

- Root [`MANIFEST_SHA256.csv`](../MANIFEST_SHA256.csv) is the **August 12 historical freeze**; the frozen README at that moment differed from later August 13 and October README versions. Do not use it as an all-files integrity check on current `main` or edit it to match today's README.
- [`manifests/OCTOBER_2026_SHA256.csv`](../manifests/OCTOBER_2026_SHA256.csv) covers the October release files maintained through subsequent documentation changes.
- [`manifests/SOURCE_AND_CODING_EXTENSION_SHA256.csv`](../manifests/SOURCE_AND_CODING_EXTENSION_SHA256.csv) covers the source/coder extension.
- Separate manifests protect the [timestamp sensitivity](../manifests/TIMESTAMP_EXCEPTION_SENSITIVITY_SHA256.csv) and [PDF content audit](../manifests/DECEMBER_2025_EXACT_CLOCK_PDF_AUDIT_SHA256.csv).
- [`manifests/DOCUMENTATION_INDEX_2026-10-29_SHA256.csv`](../manifests/DOCUMENTATION_INDEX_2026-10-29_SHA256.csv) verifies the current index, root README, and the two current README-dependent manifests. It is not a replacement for the August manifest.

**Version policy:** preserve August freeze artifacts; place later validations or corrected documentation in separately identified current materials. Do not relabel historical results as current or modify the paper's estimates without a separately justified empirical correction.
