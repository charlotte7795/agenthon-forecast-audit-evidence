# Contracts of the nine historical synthetic tests

This document was derived by reading `test_semantics_only.py` (SHA-256 `49ff703416f2a5fae82a9d34529957c39c3a9c1d0ab65eeff86c653d6ff6086f`). The historical test record in `synthetic-tests.json` reports nine passed, zero failed. The test code and forecast implementations are **not included** in this aggregation-only package. Its `verify` and `reproduce` commands do **not rerun these tests**. No new prediction was generated to prepare this document.

Unless a row states otherwise, the synthetic fixture contains 90 business dates from 2001-01-02, generated sinusoidal simple returns, factor source `factors_daily`, and horizons 1, 7 and 21. Level fixtures cumulatively sum those innovations around a positive starting level. These are generated fixtures, not actual panels or outcomes.

1. **`test_level_exact_starter_parity_rates_and_fx`** — Source lines 30–36. Input: two generated level assets, tested separately under `rates_daily` and `g10_fx_daily`; 101 draws, seed 13. Assertions: the ablation's sample array is exactly equal to the historical starter's `_draw` output, and the complete metadata dictionaries are equal.

2. **`test_factor_log1p_scale_zero_anchor_and_endpoint_rng`** — Lines 38–50. Input: one generated factor-return asset; 101 draws, seed 13. The expected sample standard deviation is calculated from `log1p(values[1:])` with `ddof=1`; a separately constructed RNG draws a fresh Gaussian array for each horizon and scales it by that standard deviation and `sqrt(h)`. Assertions: samples agree with this construction at `rtol=2e-15`, `atol=1e-16`; the anchor is exactly zero; retained history has 89 rows; reported daily standard deviation agrees to 15 decimal places.

3. **`test_first_row_and_large_gap_keep_starter_date_mask`** — Lines 52–63. Input: 100 generated factor observations, with dates from row 50 onward shifted by 366 days; the first and gap-start returns are set to 0.8 and -0.4. Assertions: 98 history rows remain, and reported standard deviation matches `log1p` returns with precisely rows 0 and 50 deleted, to 15 decimal places. This tests the specified date mask on this fixture, not every possible gap pattern.

4. **`test_shared_available_dates_are_intersected`** — Lines 65–70. Input: two generated factor assets, with two observations removed from the second asset (combined-frame indices 100 and 101). Assertion: the reported shared valid history has 87 rows. This test asserts that count; it does not separately assert every covariance entry.

5. **`test_constant_returns_do_not_become_last_return_anchor`** — Lines 72–77. Input: the single asset's 90 generated returns are replaced by constant 0.02; 100 draws, seed 3. Assertions: the reported anchor is exactly zero and all samples are numerically zero at `rtol=0`, `atol=1e-15`. This checks the retained zero-drift convention in the fixture, not forecast accuracy.

6. **`test_future_appending_and_input_immutability`** — Lines 79–90. Input: two generated factor assets; 100 draws, seed 3. Assertions after the first call: panels remain frame-equal to their deep copies and the card remains equal to its copy. Two extreme observations, -2 and 1000, are then appended seven calendar days after the unchanged `asof`; samples are exactly equal to those before appending. This verifies this future-row perturbation and the first call's input immutability.

7. **`test_same_seed_is_exact`** — Lines 92–96. Input: the same generated two-asset fixture is called twice with 100 draws and seed 3. Assertion: sample arrays are exactly equal. The test does not establish repeatability across environments, BLAS implementations or numerical-library versions.

8. **`test_invalid_factor_return_rejected`** — Lines 98–102. Input: one in-cutoff factor return at row 10 is set to exactly -1. Assertion: prediction raises `ValueError` whose message matches `exceed -1`. This is the explicitly tested boundary value; it is not an exhaustive invalid-input test.

9. **`test_unknown_return_source_rejected`** — Lines 104–107. Input: a card still declares the factor-style `log_return` target, while its generated panel is labeled `g10_fx_daily`. Assertion: prediction raises `ValueError` whose message matches `factors_daily`.

These contracts describe the assertions present in the historical source, with its recorded source hash. They do not prove historical source-import identity for earlier experiments, predictive skill, real-time availability, calibrated coverage, or equivalence to the subsequently corrected organizer CLI.
