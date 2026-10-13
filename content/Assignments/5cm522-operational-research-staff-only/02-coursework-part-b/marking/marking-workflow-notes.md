# 5CM522 CW Part B Marking Workflow Notes

## Purpose
Use these notes to keep the marking round calibrated, fair, and moderation-friendly.

## Calibration Before Full Marking
Before marking the full set, run the full template on 3 repos:
- one stronger submission
- one middling submission
- one weaker submission

Also run one quick numerical sanity pass on any notebook reporting unusually large profit values:
- regenerate the student's dataset with `generate_data.py`
- reconstruct the pre-missing true demand if needed
- compute a rough gross-demand ceiling as `sum(true zone demand) × margin_per_unit`
- treat any reported net profit far above that ceiling as a serious warning sign rather than a strong result
- if this happens, say so explicitly in both staff and student notes and check for double counting, revenue/profit confusion, inconsistent units, or over-permissive allocation logic
- if the notebook is still borderline, run a tighter reachability version of the same check using only zones that are within at least one store's service radius
- if the reported profit exceeds even that reachable-demand ceiling, treat it as strong evidence that the model is serving too much demand relative to the operational rule

For each calibration repo:
- complete the full per-student template
- assign provisional marks by criterion
- note where the guide felt ambiguous or too slow
- tighten any wording only after all 3 have been tested

Calibration check:
- the workflow should be usable in roughly 10-15 minutes per student
- the same evidence should point clearly to the same broad grade band on a second pass
- feedback should still sound specific rather than pre-written

## Rule For Broken Notebooks
- Record the break point factually.
- Mark Technical Quality and Reproducibility down in line with the rubric.
- Do not assume poor quality in other criteria where visible evidence already exists.
- Only reduce other criteria where the break genuinely prevents judgement.
- Distinguish between "weak work" and "evidence unavailable because the notebook is broken."

## Rule For Alternative Valid Methods
- Mark against the rubric, not against the hinted method in the scaffold.
- Accept ILP, MILP, heuristic, simulation, or hybrid approaches if they are clearly defined, justified, and interpreted coherently.
- Do not penalise students for using a simpler method if it is valid and well explained.
- Do penalise when the method is so under-defined that the result cannot be trusted.

## Dataset Calibration Note For Forecasting
- The generated student datasets are intentionally noisy and only partly correlated.
- Demand is perturbed by student-specific multipliers plus multiplicative noise, so a weak or even negative `R^2` can still be consistent with the task design.
- Do not mark forecasting mainly on headline fit metrics such as `R^2`, MAE, RMSE, or MSE in isolation.
- Give credit for good data-science process: sensible feature choices, appropriate validation, honest interpretation of weak fit, discussion of limitations, and careful downstream use of the forecast.
- Reduce marks when students overclaim, ignore poor fit, skip validation, or treat unreliable forecasts as certain.

## Rule For Understanding Versus Sophistication
- Separate technical ambition from demonstrated understanding.
- A polished or sophisticated solution should not score highly on justification if the student does not explain it coherently.
- A simpler solution can still score strongly if it is appropriate, justified, and well interpreted.
- If there is a noticeable mismatch between sophistication and explanation, log a factual concern note for potential viva follow-up.

## Rule For Consistent Concern Logging
Use factual language only. Record:
- what is missing
- what failed to run
- what was unclear
- what prompted concern

Avoid:
- making misconduct conclusions in marking notes
- vague language such as "seems suspicious" without evidence
- blending concern notes into rubric-based quality comments

## Standard Fairness Checks For Every Repo
- Did the notebook likely run top-to-bottom?
- Is demand allocation explicitly defined?
- Is the same allocation logic used in baselines and optimisation?
- Are scenarios quantitative rather than purely narrative?
- Do the conclusions connect technical results to business implications?

## Rule For Explaining Marks
- For every notebook criterion, record not only what was good, but also what kept the mark below the next band.
- Student-facing feedback should let the student see why they received that section mark, not just whether the work was generally strong or weak.
- Internal notes should distinguish clearly between:
  - evidence that earned the mark
  - evidence that prevented a higher mark
  - the kind of stronger evidence that would have moved the mark upward

## Suggested Working Rhythm
1. Open the repo and confirm submission completeness.
2. Skim notebook structure before reading details.
3. Mark notebook criteria in rubric order.
4. Review slides/video immediately after the notebook so the recommendation is still fresh.
5. Write feedback from evidence, then enter the final mark in the cohort's copy of `part-b-marking-grid-template.xlsx`.

## After 5-10 Scripts
Pause and review whether:
- you are using the full mark range
- one criterion is drifting stricter or looser than intended
- broken notebooks are being treated consistently
- feedback comments are staying specific

If needed, recalibrate using one already-marked stronger script and one weaker script.
