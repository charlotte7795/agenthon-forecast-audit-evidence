# Fixed paper extension: family decomposition, target handling, later-window check

Written before generating any new forecasts in this extension. The user's September 29 New York instruction explicitly permits the 124-window evaluation tonight if its workload is reasonable. Existing timing records imply minutes of computation, with freezing, verification and interpretation taking longer. No new paid resources or external submission is authorized or needed.

## Fixed questions and methods

1. Reaggregate saved development losses by factor log returns, FX levels and rate levels using the original duplicate-cell then series-year then equal-series rules. Retain mixed-source joint grids as a separate group; do not invent component joint losses.
2. Add one target-handling comparator to the historical public starter. For factor cumulative-log-return cards only, use log(1+r) innovations on exactly the old differencing-valid dates and zero anchor. Preserve zero drift, full history, sample covariance construction, PSD nudge, independent horizon draws and RNG order. Level cards call the unchanged old starter. No new window, coefficient, seed, parameter search or shared-path ablation is introduced.
3. Re-execute the three primary historical methods (public starter, semantic Gaussian, default resampling) on the fixed 886 development folds, together with that one fixed comparator. Compare regenerated primary losses to the saved originals. This is new byte-attested execution and does not retroactively repair the old import-time identity gap.
4. If synthetic tests and the development reproduction pass, execute the same four frozen methods once on all 124 original later-window folds. Do not select a different method after the development extension or after seeing the later results. Report all successes, failures and ratios, favorable or unfavorable.

## Frozen evaluation

- Preserve plan SHA256 `4abc837d6d0cde8a81880441248eeb87a5f98c5399e855143885e87b7b98b1d8`, original exclusions and all 886/124 memberships. No new split or target reconstruction across cards.
- Default historical predictor is the exactly reconstructed completion-state SHA256 `65bc434a89691c958b590a04ed451e69b46321aac20fd5aff2b9efb8ef5f26f3`, not the current competition rank variant. Reconstruction history is retained separately.
- Four methods: `official-floor` (paper display name public starter), `semantics-only`, `semantic-gaussian`, `block-bootstrap`. N=1000 draws, seed=20260914; original b=5, recency=.6, half-life=63 and other historical defaults unchanged.
- Use original exact endpoint truth and same-card at-or-before-origin inputs; strip future prose/identifiers, with no House/model/text calls. Rolling refits use only each origin's available rows.
- Fair ensemble CRPS, four-quantile tail pinball and raw-unit p=.5 variogram score. Duplicate marginal observations are averaged; horizons within series-year, years within series, and series ratios are equally weighted. Joint ratios average within grid then across positive-baseline grids; zero-baseline grids are counted separately.
- Reuse the original exploratory common-year resampling algorithm and seed for interval diagnostics; no new confidence claim from six later calendar years, sparse support or selected development methods.
- Capture runner, evaluator, predictor, ablation, imported scoring/reference source hashes and dependency versions before prediction, then verify unchanged at completion. Check panel file hashes against original plan and card metadata hashes against the freeze before load.
- All input/prediction errors remain in the per-model planned denominator. Incomplete comparisons cannot establish a winner. No retry of model failures or selective exclusion. Save all terminal results before aggregation.

## One-time status and interpretation

Immediately before the first later-window data load, create exclusive `outputs/apex-validation/test-opened.json` and its seal. An existing marker prevents another untouched evaluation. The original October 9–11 T2 untouched-holdout plan is superseded once this is opened; future competition evaluation must not relabel these windows unseen. T1's 18 reserved problems are unaffected and remain closed.

These are retrospectively partitioned public histories, not organizer-sealed data or pristine real-time vintages. The 124 metadata rows cover 2019–2024, 33 grids, 18 series and 83 series-years; their support differs from development. Report later-window results separately, alongside matched-support development diagnostics if needed, not as proof of a causal regime effect or competition eligibility. No method or competition parameter will be changed on the basis of these later-window outcomes.

The paper remains an evaluation study. No official leaderboard score is added. Public research repository publication and paper submission are outside this run.
