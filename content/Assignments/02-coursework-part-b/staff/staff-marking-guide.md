# 5CM522 CW Part B Staff Marking Guide

## Purpose
Use this guide live while marking each submission. It is designed to keep marking fast, fair, and directly tied to the published rubric rather than to any single "expected" modelling method.

The assessed structure is:
- `notebook.ipynb` worth 80% of the coursework mark
- executive slide deck worth part of the 20% communication component
- 10 +/- 1 minute video worth part of the 20% communication component
- AI-use acknowledgement as a required submission item

The default notebook evidence structure is:
- Milestone 1 -> Demand Modelling and Forecasting
- Milestones 2-4 -> Decision Modelling and Optimisation
- Milestone 5 -> Integration, Scenarios and Insight
- Reflection and Executive Summary -> Understanding and Justification

## Dataset Calibration Note
The student datasets are designed to be only partly correlated. The generator applies student-specific multipliers and multiplicative noise, so a poor `R^2` or high error metric may be expected. Mark Milestone 1 primarily on process and judgement:
- sensible feature use and model choice
- real validation and metric interpretation
- honest acknowledgement of weak fit or uncertainty
- appropriate caution in how forecasts are used downstream

Do not over-penalise a notebook simply because the forecast is not highly predictive.

## Profit Sanity Note
For Milestones 2-5, it is also worth running a basic numerical sanity check when reported profits look extreme.

A useful rough ceiling is:
- `sum(true zone demand) × margin_per_unit`

This is not a realistic target profit. It is only a gross-demand upper bound before service costs and opening costs are subtracted.

If a student's reported net profit sits far above that ceiling, treat this as a serious warning sign for:
- demand double counting
- revenue/profit confusion
- inconsistent units
- infeasible allocation logic
- scenario recalibration errors

A stronger follow-up check is:
- `sum(true zone demand for zones within at least one store's service radius) × margin_per_unit`

If a reported profit exceeds this tighter reachable-demand ceiling, the notebook is likely serving too much demand relative to the operational reachability rule, even if it passed the looser gross-demand check.

## Recommended Marking Order
1. Check submission completeness.
2. Check notebook reproducibility and structure.
3. Mark notebook criteria in rubric order.
4. Mark slides and video.
5. Write concise strengths, weaknesses, and actionable feedback.

## 10-15 Minute Per-Student Workflow

### Minute 0-2: Submission Completeness
Check for:
- `notebook.ipynb`
- slide deck PDF
- video submission
- AI-use acknowledgement or prompt/chat evidence

Record separately:
- missing item
- present but unusable item
- present and usable item

Do not compensate for a missing component by inflating another component.

### Minute 2-4: Notebook Reproducibility and Structure
Check:
- notebook appears to follow the supplied milestone structure
- student ID is set
- outputs are present
- explanations exist alongside code
- the work looks runnable top-to-bottom without manual repair

Look specifically for:
- explicit demand allocation rule
- same allocation logic used in baseline and optimisation sections
- labelled plots/tables
- final conclusions linked to business implications

If the notebook is broken:
- note exactly where evidence becomes unavailable
- mark Technical Quality and Reproducibility accordingly
- only reduce other criteria where the break genuinely prevents evidence

### Minute 4-10: Mark the Notebook Criteria

#### 1. Demand Modelling and Forecasting (20%)
Prompt yourself:
- Is there a sensible forecasting task definition?
- Are features chosen and justified?
- Is the model choice appropriate to the data/problem?
- Is there validation beyond simply fitting and reporting output?
- Are metrics interpreted, not just printed?
- Are limitations or uncertainty acknowledged?
- If fit is weak, does the student handle that honestly and still use the forecast responsibly?

#### 2. Decision Modelling and Optimisation (20%)
Prompt yourself:
- Is the decision model clearly defined?
- Are objective, decision variables, and constraints understandable?
- Is the method justified, even if simple?
- Does the model reflect opening costs, service/distance costs, capacity, and allocation logic?
- Do results look economically coherent?

#### 3. Integration, Scenarios and Insight (20%)
Prompt yourself:
- Do forecast outputs actually feed the decision model?
- Are at least two scenarios analysed quantitatively?
- Are trade-offs explained clearly?
- Does the student move from results to business insight?

#### 4. Understanding and Justification (15%)
Prompt yourself:
- Does the notebook explain why choices were made?
- Can you see the student's reasoning, not just outputs?
- Do reflection and executive summary show ownership of the work?
- Is there any mismatch between technical sophistication and demonstrated understanding?

#### 5. Technical Quality and Reproducibility (5%)
Prompt yourself:
- Would `Restart & Run All` likely work without intervention?
- Is the notebook cleanly structured?
- Are outputs labelled and readable?
- Is the code organised enough to follow the logic?

### Minute 10-12: Mark Executive Communication (20%)
Check the slides/video against the brief:
- problem and opportunity
- recommendation
- value versus baseline
- trade-offs and scenarios
- risks and next steps

Judge whether the communication is executive-facing rather than overly technical.

### Minute 12-15: Write Feedback
Aim for:
- 2-3 specific strengths
- 2-3 specific weaknesses
- 1-2 actionable next steps

Use visible evidence. Avoid generic praise or criticism.

For each notebook criterion, capture three separate ideas in your notes:
- why this mark was awarded
- what stopped it being higher
- what stronger evidence would have looked like

This is especially important for Milestone 1. A weak `R^2` should not be treated as a cap by itself, but if the mark is not in the top band, the notes should say exactly what is missing beyond raw fit, such as limited model comparison, shallow diagnostics, weak error interrogation, or insufficient uncertainty analysis.

## Fairness Rules

### What To Look For
- valid methods that are clearly defined, justified, and interpreted
- consistency between assumptions in baselines and optimisation
- evidence of quantitative reasoning
- business interpretation, not only technical output
- explicit acknowledgement of assumptions and limitations

### What Not To Over-Penalise
- a different valid optimisation approach from the hints or examples
- simple models that are well justified and correctly interpreted
- imperfect coding style when the work is still understandable and reproducible
- minor presentation roughness if the underlying reasoning is clear
- students not using every available dataset column

## Quick Decision Anchors
- First: clear method, justified choices, quantitative validation, coherent insight, strong business communication
- 2:1: solid and mostly clear, with minor gaps in depth or justification
- 2:2: works at a basic level, but limited reasoning, weak interpretation, or shallow scenario work
- Third: partial, weakly justified, or difficult to trust
- Fail: missing, incoherent, or not meaningfully addressing the task

## Concern Flags
Record separately if any of the following arise:
- missing AI-use acknowledgement
- major mismatch between sophistication and understanding
- non-reproducible notebook
- unclear ownership/originality concerns
- missing slides or video

Use a short factual note, not a conclusion about misconduct.
