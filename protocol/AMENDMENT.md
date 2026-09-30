# Before-opening amendment: evaluate the current frozen implementation

Written after inspecting the new 886-window development run and its replay discrepancy, but before generating any forecasts or scores on the original 124 later windows. The original PLAN.md, freeze.json, opening controller, failed reproduction.json, and diagnostic are preserved. This amendment does not turn that failed replay into a pass or loosen its tolerance.

## Reason and changed research question

All four methods completed 886/886 development windows without failures. The resampling losses reproduce exactly; public-starter differences are at numerical rounding scale. Semantic-Gaussian losses differ on 88 windows, all with at least three assets. In one bounded 2017 development example, a covariance-equivalent eigenvector sign change reproduces the old three losses to 4.44e-16. This identifies a finite-simulation sensitivity in that example, not the cause of every discrepant window or the system-level origin of the change. No sign convention is changed or selected for the actual experiment.

The replacement question is: how do these four current, source-attested implementations compare on the original later windows? It is not an exact reproduction of the historical Gaussian samples. The new later results must be paired with the newly generated 886 development results, not the old Gaussian results. Historical results remain separately labeled.

## Unchanged experimental choices

The four methods, predictor/evaluator/ablation and imported reference/scoring sources, parameters, 1000 draws, seed 20260914, all original memberships and exclusions, same-card historical inputs, scoring, aggregation, and failure accounting remain unchanged from the first freeze. Only the opening controller and its documentation change. No additional development run, seed search, symbol/sign replacement, or selective retry is allowed. Nine synthetic target-handling checks passed; the level ablation exactly matches the starter on all relevant development losses. One method's replay discrepancy cannot be hidden in a successful subset denominator.

## Replacement opening prerequisites

Before opening, bind the first freeze, completed development run, complete four-method coverage, failed replay report, synthetic-test record and Gaussian diagnostic by hash. Verify every source from the first freeze unchanged except the archived opening controller; freeze the new controller and amendment separately. The source algorithm and aggregation functions are unchanged. The later run requires this explicit amendment, a still-closed global marker, and the recorded complete development run; it does not require or claim a successful old Gaussian replay.

Run all four methods once on all 124 windows, retain all outcomes and failures, then verify frozen source identity again. Mark all 124 windows consumed globally before their first data load. Do not use their losses for method or competition tuning and do not later describe them as an untouched October holdout. T1's 18 reserved tasks remain closed. Any incomplete run remains incomplete rather than being retried as fresh evidence.

This is an amended, before-opening-frozen later historical evaluation. It is not a fully preregistered study, a real-time vintage test, an organizer-sealed test, or an independent replication of the old source identity. Calendar and support differences limit development/later comparisons. The author's current instruction authorizes this one manageable evaluation; no paid resources or external paper submission are involved.
