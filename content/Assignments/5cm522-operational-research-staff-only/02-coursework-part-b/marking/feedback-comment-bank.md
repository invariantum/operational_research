# 5CM522 CW Part B Feedback Comment Bank

## How To Use
Mix and adapt these comments so feedback stays specific. Pick comments that match the evidence and add one short reference to the student's actual work.

## Submission And Reproducibility

### Strengths
- The submission was complete and easy to follow, which supported efficient marking and showed good attention to the brief.
- The notebook was clearly structured around the milestones and presented evidence in a way that made the modelling process reproducible.
- Outputs were labelled clearly, making it straightforward to connect technical results to the final recommendation.

### Weaknesses
- A required submission component was missing or incomplete, which limited the available evidence for full assessment.
- The notebook was difficult to reproduce reliably because it appeared to depend on execution order or manual intervention.
- Some outputs were presented without enough labelling or context, which reduced clarity even where the underlying work was sound.

### Next Steps
- Before submission, use `Restart & Run All` and fix any ordering or hidden-state issues.
- Treat submission completeness as part of the assessment task and check that slides, video, and AI-use acknowledgement are all included.
- Improve output labelling so each table or figure supports a specific interpretation.

## Demand Modelling And Forecasting

### First / Strong 2:1
- Your forecasting approach was appropriate to the problem and supported by sensible feature use, validation, and clear interpretation of performance.
- You moved beyond reporting metrics by explaining what the model performance means for trust in the downstream optimisation stage.
- Limitations and uncertainty were acknowledged realistically, which strengthened the credibility of the forecasting section.

### Mid / Low 2:1 / 2:2
- The forecasting model was workable and relevant, but the justification for feature selection and model choice needed more depth.
- Metrics were reported appropriately, although the interpretation of what they imply for decision quality remained fairly limited.
- The section demonstrated a basic predictive workflow, but it would benefit from clearer explanation of uncertainty and model limitations.

### Third / Fail
- The forecasting stage was weakly justified, making it difficult to judge whether the predictions were reliable enough for later decisions.
- Limited validation and interpretation reduced confidence in the demand estimates used throughout the notebook.
- The forecasting work did not yet provide a meaningful or credible basis for the optimisation stage.

### Next Steps
- Explain why the chosen predictors are plausible drivers of demand rather than simply available columns.
- Link model performance to business risk by discussing what forecast error might mean for store-opening decisions.
- Add a clearer validation rationale and explicitly discuss uncertainty.

## Decision Modelling And Optimisation

### First / Strong 2:1
- The optimisation model was clearly formulated, economically coherent, and well aligned to the business objective.
- Decision variables, constraints, and objective were explained in a way that made the logic of the model easy to follow.
- You validated the optimisation output sensibly against baseline expectations, which improved trust in the recommendation.

### Mid / Low 2:1 / 2:2
- The decision model was functional, but some aspects of the formulation or justification remained under-explained.
- The optimisation logic was reasonable overall, although the economic interpretation and validation of results could have been stronger.
- The model addressed the core problem, but some assumptions were accepted without enough discussion.

### Third / Fail
- The decision model was too ad hoc or under-defined to provide a convincing recommendation.
- Important aspects of the problem formulation were unclear, which weakened confidence in the reported result.
- The optimisation section did not yet show a meaningful or well-justified decision model.

### Next Steps
- State objective, variables, and key constraints explicitly before presenting results.
- Add a short economic sense check to show why the result is plausible.
- Make the demand allocation rule fully explicit and use it consistently across baselines and optimisation.

## Integration, Scenarios And Insight

### First / Strong 2:1
- The notebook integrated forecasting and optimisation effectively, and the scenario analysis added genuine decision insight.
- Trade-offs were articulated clearly, particularly in showing how the recommendation changes under alternative assumptions.
- The analysis moved beyond raw results to explain the operational meaning of the recommended network.

### Mid / Low 2:1 / 2:2
- Forecasting and optimisation were linked, but the integration was more functional than analytically insightful.
- Scenario analysis was present, although it remained somewhat limited in depth or comparison.
- The section showed some awareness of trade-offs, but the business insight could have been developed further.

### Third / Fail
- The integration between predictive and decision stages was minimal, which reduced the coherence of the overall analysis.
- Scenario analysis was shallow or largely descriptive, so the robustness of the recommendation remained unclear.
- The notebook did not yet show enough insight into trade-offs or sensitivity to support a strong business recommendation.

### Next Steps
- Quantify scenario differences clearly rather than describing them narratively.
- Use scenarios to test robustness, not only to demonstrate that extra work was done.
- Make trade-offs explicit: profit, coverage, utilisation, and risk.

## Understanding And Justification

### First / Strong 2:1
- The notebook demonstrated clear ownership of the modelling choices and explained the reasoning behind them effectively.
- Your explanations connected methods, results, and business implications in a coherent way throughout the notebook.
- The reflection and summary showed strong understanding of both strengths and limitations in the work.

### Mid / Low 2:1 / 2:2
- The notebook included explanation throughout, but parts of the reasoning remained more descriptive than analytical.
- You showed a workable understanding of the process, though some key choices would benefit from fuller justification.
- The reflection identified limitations, but the implications for the quality of the recommendation were not always fully developed.

### Third / Fail
- Explanation was limited or inconsistent, making it difficult to see the reasoning behind important modelling choices.
- There was not enough evidence of understanding to support the technical work shown.
- The notebook would be stronger if the student more clearly justified methods and interpreted results in their own terms.

### Next Steps
- For each major modelling choice, answer "why this approach here?"
- Use the reflection to discuss how assumptions may have shaped the recommendation.
- Strengthen the executive summary so it presents a decision argument, not just a recap.

## Executive Communication

### Strong Business Communication
- The slides and video communicated the recommendation clearly to a non-technical audience and maintained focus on value, trade-offs, and risks.
- The presentation used evidence effectively to support the recommendation without becoming overly technical.
- The recommendation, its value relative to baseline, and the next steps were all communicated clearly and persuasively.

### Adequate / Mixed Communication
- The presentation communicated the main result, but the business value and trade-offs could have been made clearer for an executive audience.
- The slides/video were understandable overall, though some sections relied too heavily on technical detail rather than decision-focused communication.
- The recommendation was present, but the supporting case for why it should be adopted needed sharper presentation.

### Weak / Missing Communication
- The presentation was unclear, incomplete, or insufficiently focused on the business decision.
- Slides/video did not yet provide a strong executive-level recommendation supported by evidence.
- Missing or unusable communication artefacts limited the evidence available for this criterion.

### Next Steps
- Structure the presentation explicitly around decision, recommendation, value, trade-offs, and risks.
- Reduce technical detail on slides and use that space for decision-relevant evidence.
- Compare the recommendation to a baseline so value is immediately visible.

## AI Use And Academic Concern Wording

### Missing AI Acknowledgement
- The required acknowledgement of AI-tool use was not present in the submission materials, so this should be treated as a missing required component.

### Viva / Understanding Concern
- There is a notable gap between the sophistication of some technical elements and the level of explanation provided, so this submission may warrant closer scrutiny of understanding.

### Neutral Logging Language
- Evidence of concern should be logged factually and separately from the academic judgement on quality.
