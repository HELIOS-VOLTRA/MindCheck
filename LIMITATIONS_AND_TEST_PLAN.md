# Limitations and Test Plan

## Current scope

- A local Streamlit dashboard.
- A fixed synthetic dataset of 30 profiles × 30 daily observations.
- Explicit rules comparing a 7-observation baseline with the latest 3 observations.
- Charts, a per-indicator comparison table, and CSV downloads.

## Not included in Week 1

- Physical hardware or sensor readings.
- Real student data, clinical screening, diagnosis, or recommendations for treatment.
- Validated psychometric questionnaires or clinically approved thresholds.
- Cloud hosting, authentication, or production-grade security.
- A trained predictive model or an LLM-based evaluator.

## Main limitations

1. **Synthetic data:** useful for exercising code paths, but not evidence of performance on real students.
2. **Illustrative thresholds:** thresholds are engineering examples, not evidence-based clinical cut-offs.
3. **Small fixed windows:** a 7-observation baseline and 3-observation recent window may be sensitive to noise and are not universally appropriate.
4. **Self-report context:** mood, stress, sleep, fatigue and workload are simplified fields. Definitions and collection frequency would need to be reviewed.
5. **No causal inference:** observed changes do not prove why a change occurred.
6. **No safety/clinical workflow:** this is not a crisis-monitoring system and should not be used to make decisions about a real person's safety.

## Week 1 verification checklist

| Test | Expected result |
|---|---|
| Stable profile | No demo threshold crossing |
| Stress and sleep both shift persistently | Multiple changes above demo thresholds |
| Stress alone shifts | One change above a demo threshold |
| Too few observations | Analysis says more check-ins are needed |
| Change selected profile | Charts and table update to selected profile |
| Download selected profile | CSV downloads and opens |
| Delete or move dataset temporarily | App displays a helpful missing-file message |

## Evidence to save

- Screenshot of the main dashboard.
- Screenshot of a baseline comparison table.
- Screenshot of `pytest` results.
- A short list of bugs encountered and fixes made.
- A copy of the app version used in the panel demo.
