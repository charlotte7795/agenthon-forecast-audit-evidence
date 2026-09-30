# Paper evidence package: reproduce saved-loss aggregations

This evidence package accompanies *Auditing Financial Forecast Benchmarks: Target Semantics, Baseline Choice, and Historical Validation in Agenthon 2026*. It reconstructs point estimates in Tables 2–4 from saved per-cell and per-grid losses. The manuscript has not been submitted.

## Run in a fresh directory

Only Python 3.8 or newer and its standard library are required. No installation, network, account, original checkout, NumPy, pandas, model, or data service is needed. The script locates inputs relative to itself; the working directory is irrelevant.

```sh
python3 -I reproduce.py verify
python3 -I reproduce.py reproduce > reproduced-tables.json
```

`verify` checks SHA-256 and byte counts of every distribution file listed in `manifest.json`. `reproduce` also checks integrity, reconstructs tables from losses, checks all planned windows and cells, and compares the independently saved table values with an absolute tolerance of 2e-14. It exits nonzero on a mismatch. JSON output contains full-precision tables, coverage, and every joint grid's denominator and ratio. Expected tables are read only after reconstruction and do not supply the computed estimates. A hash manifest establishes consistency with this copy, not external authenticity or a historical timestamp.

Table 2 contains resampling relative to three references in development and later windows. Table 3 contains the development factor/FX/rate family ratios. Table 4 contains the post-opening, descriptive yearly factor target-correction diagnostic. Table 4 distinguishes an observed grid with a zero joint denominator (2023) from no factor observations (2024); neither is a zero loss ratio.

The output also reconstructs the whole-period, pure-factor corrected/starter joint ratios discussed in the text: approximately 0.5809 in development (five defined grids) and 1.2259 later (three defined grids). These use the same grid aggregation as Table 2, not an average of Table 4's yearly ratios.

## Aggregation and denominators

For marginal CRPS and tail losses, average repeated source/asset/origin/horizon cells within method, then average cells within source/asset/year. For each source/asset, divide candidate mean annual loss by baseline mean annual loss, then equally average those ratios. Family tables apply the same rule within the declared source/target family. Ratios are not ratios of previously aggregated ratios.

For joint loss, pair the same grid/origin windows, average within grid, divide by the baseline grid mean if positive, then equally average defined grid ratios. All zero-baseline grids remain in the emitted details with a null ratio. Development has 63 grids (30 positive, 33 zero); later has 33 (17 positive, 16 zero). Raw variogram coordinate units are unchanged.

For Table 4, apply the same duplicate-cell and series-year reductions to factor cells, then average corrected/starter asset ratios separately within each year. Joint rows use whole pure-factor grids within each year. These varying-support annual ratios are not averaged into a replacement whole-period score.

The four stored method keys are `official-floor` (the historical public starter, not a hosted normalization baseline), `semantics-only` (target-corrected starter), `semantic-gaussian`, and `block-bootstrap` (resampling). Each completed all 886 development and 124 later windows with zero failures. The package retains full window lists, all four methods' losses and failure ledgers. The script derives coverage from the window list and outcome records, checks equal support, and refuses a successful-subset table if failures exist. It does not define a failure penalty for hypothetical incomplete runs.

## Files and provenance

- `losses/`: byte-for-byte cell losses, group losses, planned windows, run identities and failure ledgers for both periods. No raw panel, realized outcome, forecast tensor or credential is included.
- `series-list.json`: source/asset/year membership, derived from the losses.
- `protocol/`: original extension plan, before-opening amendment, both original freezes, failed historical replay record, bounded Gaussian diagnostic and nine synthetic-check record.
- `protocol/synthetic-check-contracts.md`: derived documentation of each historical test's exact name, synthetic input and asserted property. The historical test code is not distributed or rerun by this package.
- `historical-records/`: original terminal summaries and family/year diagnostics. Their source hashes identify the inputs used at the time.
- `provenance.json`: original-to-package relative-name and SHA-256 mapping. No redaction was required for this whitelist. Original protocol text and freezes are preserved verbatim. Paths inside those historical records are informational identifiers, not runtime dependencies. Some referenced source/data artifacts are intentionally not distributed.
- `expected-tables.json`: terminal table values used solely for a final cross-check.
- `manifest.json`: hashes and sizes for all distribution files except itself.

Forecast algorithms and raw data are intentionally absent. Their original identities and configuration (1,000 draws, seed 20260914, fixed methods) remain in the freezes. This package reproduces aggregation, not forecast generation, score calculation from draws/outcomes, the source identity of the old run, or the historical data acquisition. Original confidence intervals are retained in historical summaries but are **not regenerated** by this standard-library aggregator; they remain conditional exploratory year-resampling diagnostics.

## Scientific limits

The later partition was opened once after the documented amendment and is permanently consumed. The amendment followed a failed Gaussian finite-sample replay on 88 development windows; that failure remains false, not relabeled as passed. The single-case covariance-sign diagnostic does not explain all discrepancies. Later comparisons use the new development execution, not the old Gaussian losses.

Both periods are retrospectively partitioned public histories, not pristine real-time vintages or organizer-sealed tests. Series, grids, horizons and calendar support overlap or differ; they are not independent replications. Six later years and sparse supports limit uncertainty claims. Development was reused for method selection. Correct target mapping does not guarantee lower realized losses: adverse later starter and ablation comparisons are retained. No official competition score, trading return, new prediction, calibrated coverage guarantee or superiority claim follows from running this package.

## Version and license

This is the first public evidence snapshot for the manuscript. Use a fixed commit URL when citing the records; the manifest checks file identity within that snapshot. Historical freezes describe the original execution, not a public timestamp predating this release.

The original aggregation code (`reproduce.py`) is MIT-licensed; see `LICENSE`. The license applies to that code and does not relicense upstream datasets or forecast implementations, which are not distributed here. Research records are supplied for inspection and verification. No public or private raw data is redistributed.
