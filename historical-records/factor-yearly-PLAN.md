# Fixed stored-loss diagnostic

Compare `semantics-only` (target-corrected starter) with `official-floor` (historical starter) for the `factors_daily` source in the already completed `work/paper-depth-20260929/later-124` run. No new forecast, panel/target read, fitting, seed change, model choice or held-out evaluation is permitted.

For each calendar year 2019–2024, average duplicate marginal losses by `(source, asset, origin, horizon, year, model)`, then average cells within each asset-year. Form each paired asset-year's corrected/starter mean-loss ratio and average defined ratios equally across assets within that year. CRPS and tail retain their original stored metric definitions.

For joint scores use only whole pure-factor grids. Average each grid-year's stored joint losses, form its corrected/starter ratio, then average equally over grids with positive baseline loss in that year. Report zero-baseline grids as undefined, not as zero ratios, and retain years with no factor observations as missing.

Report per-year paired asset and grid denominators, available deduplicated cells, lower/higher/tied ratio counts and shares among defined comparisons. Direction tolerance is 1e-12. Summarize proportions of supported years with improvement/retreat and proportions of asset-year/grid-year comparisons; these describe heterogeneous, correlated observations and do not supply independent tests.

Annual ratios must not be averaged or pooled to reproduce the original 18-series whole-split statistic or the four-factor-series whole-split statistic. The whole-split statistic weights years within a series before forming a ratio, whereas this diagnostic forms separate ratios within each year. No causal mechanism, significance claim or parameter update will be inferred.
