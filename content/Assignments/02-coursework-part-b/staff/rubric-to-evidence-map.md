# 5CM522 CW Part B Rubric To Evidence Map

## How To Use
For each criterion, mark from visible evidence in the submission. Use this map to avoid drifting into preference-marking.

## Demand Modelling and Forecasting (20%)

### Required Evidence
- a forecasting approach for missing zone demand
- feature selection or feature usage visible in the notebook
- model choice stated or inferable from code and explained
- validation approach
- metrics reported

### Strong Evidence
- features are chosen sensibly and justified
- model choice matches the problem and data size
- validation is more than a token split
- metrics are interpreted critically
- limitations, uncertainty, or data issues are discussed
- weak fit is handled honestly and does not lead to unjustified overclaiming

### Borderline Evidence
- model runs and produces predictions
- minimal or weak explanation of why the model was chosen
- metrics reported but barely interpreted
- limited discussion of assumptions or uncertainty
- low `R^2` is treated as the whole story, with little reflection on what the model can still support

### Fail-Level Evidence
- no meaningful forecasting step
- incorrect target/task setup
- predictions appear arbitrary or unexplained
- no validation or meaningless metrics

### Common Pitfalls
- printing `R^2` or RMSE without interpretation
- over-penalising or overclaiming based on `R^2` alone
- using many features without justification
- no discussion of missingness, outliers, or uncertainty
- forecasting section ending with code only and no reasoning

## Decision Modelling and Optimisation (20%)

### Required Evidence
- a decision model for store opening/allocation
- objective function tied to profit
- constraints or rules reflecting the problem
- opening costs, capacity, and allocation logic represented
- some validation or plausibility check

### Strong Evidence
- variables, parameters, objective, and constraints are clear
- method is justified even if simple
- economic logic is coherent
- results are checked against baselines or sanity tests
- allocation method is explicit and operationally meaningful

### Borderline Evidence
- model works but is partly ad hoc
- objective or constraints are only partly explained
- limited evidence of validation
- logic is plausible but not well justified

### Fail-Level Evidence
- no meaningful decision model
- choices appear manual or arbitrary
- objective does not connect to the stated business goal
- constraints missing to the point that outputs are not credible

### Common Pitfalls
- optimisation with no clear profit definition
- baselines using different allocation logic from the final model
- unexplained heuristics presented as if self-evident
- results reported with no economic sense check

## Integration, Scenarios and Insight (20%)

### Required Evidence
- forecast outputs used in the decision stage
- at least two scenarios or sensitivity checks
- some discussion of trade-offs

### Strong Evidence
- forecast meaningfully changes downstream decisions
- scenarios are quantitative and compared clearly
- trade-offs are reasoned, not merely listed
- business insight goes beyond "profit increased"

### Borderline Evidence
- basic integration is present
- scenarios exist but are shallow or repetitive
- insight is mostly descriptive

### Fail-Level Evidence
- forecasting and optimisation are effectively separate pieces
- no meaningful scenario analysis
- no trade-off reasoning

### Common Pitfalls
- scenarios that only restate the base case
- narrative scenario discussion with no rerun or quantified comparison
- optimisation recommendation presented without discussing sensitivity

## Understanding and Justification (15%)

### Required Evidence
- explanatory markdown across the notebook
- justification for core modelling choices
- interpretation of results
- reflection and executive summary completed

### Strong Evidence
- notebook reads as the student's own reasoning
- choices are explained clearly and coherently
- reflection shows awareness of assumptions, limitations, and improvements
- executive summary translates technical findings into decision logic

### Borderline Evidence
- explanation is present but mostly descriptive
- reasoning is incomplete or uneven across sections
- reflection/summary exist but are generic

### Fail-Level Evidence
- inability to explain why methods were used
- explanation absent, inconsistent, or clearly disconnected from the code/results
- strong signs the student cannot account for the work shown

### Common Pitfalls
- narration of steps without justification
- reflection that lists limitations without relating them to the model
- executive summary that repeats outputs but not implications

## Technical Quality and Reproducibility (5%)

### Required Evidence
- notebook file present and structured
- outputs visible
- reasonable evidence it can run top-to-bottom

### Strong Evidence
- likely to pass `Restart & Run All`
- clear sectioning and readable code
- labelled tables/plots
- no obvious manual patching required

### Borderline Evidence
- mostly works but has clutter, fragile ordering, or minor reproducibility concerns
- some outputs lack labels or context

### Fail-Level Evidence
- notebook is non-reproducible
- execution depends on missing steps, hidden state, or manual fixes
- organisation prevents reliable marking

### Common Pitfalls
- cells must be run out of order
- hidden dependencies on local state/files
- outputs missing from key sections

## Executive Communication (20%)

### Required Evidence
- slides and video submitted
- recommendation presented
- value, trade-offs, and risks addressed

### Strong Evidence
- executive tone rather than technical dump
- recommendation is clear and supported
- value is compared to a baseline
- scenarios, risks, and next steps are communicated clearly

### Borderline Evidence
- communication is understandable but basic
- recommendation exists but support is thin
- too much technical detail crowds out business meaning

### Fail-Level Evidence
- slides/video missing, incoherent, or not stakeholder-appropriate
- no clear recommendation
- business value not communicated

### Common Pitfalls
- reading technical notebook content to camera without synthesis
- slide deck lacks a decision
- recommendation given without risks or next steps

## Cross-Criterion Fairness Checks
Apply these to every repo:
- Has the notebook likely run top-to-bottom?
- Is the demand allocation method explicitly defined?
- Is the same allocation logic used in baselines and optimisation?
- Are scenarios quantitative rather than purely narrative?
- Do conclusions connect technical results to business implications?

If evidence is blocked by a broken notebook, say so explicitly in notes rather than assuming weakness.
