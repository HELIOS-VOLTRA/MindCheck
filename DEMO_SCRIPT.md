# MindCheck Week 1 — 3–4 Minute Demo Script

## 1. Introduce the prototype (20 seconds)
"MindCheck is our student wellbeing trend-monitoring prototype. Today we are demonstrating the software pipeline using synthetic data only. It is not a diagnostic or clinically validated tool."

## 2. Show the dashboard (40 seconds)
- Point out the number of synthetic check-ins and profiles.
- Change the student selector.
- Show how the trend graphs update.
- Explain that the values are fake and exist to test the workflow.

## 3. Explain the comparison (60–90 seconds)
"The prototype uses a transparent baseline approach. It compares the first seven observations with the latest three observations. Example thresholds are coded explicitly. Each threshold crossing is shown separately, and the summary distinguishes no crossing, one crossing, and multiple crossings."

Pick one indicator in the table and explain:
- baseline average;
- recent average;
- how the difference relates to the threshold;
- why crossing an engineering threshold is not a diagnosis.

## 4. Show a second profile (30–45 seconds)
Choose a different synthetic profile and note how the displayed pattern changes. Do not claim that the synthetic examples prove real-world accuracy.

## 5. Show a downloaded output (20 seconds)
Download the selected profile CSV or the baseline comparison table to demonstrate that the results can be inspected outside the dashboard.

## 6. Close with the next steps (20–30 seconds)
"Our immediate next steps are to improve validation, test more edge cases, get feedback on indicator selection and privacy from our guide, and only after the software is stable add the ESP32 temperature/humidity sensor as an optional extension."

## Likely guide questions

**Q: Is this burnout diagnosis?**
A: No. It is a proof-of-concept that identifies changes in synthetic self-reported indicators. Thresholds are illustrative and not clinically validated.

**Q: Why not start with a complex AI model?**
A: We are first building a transparent baseline that is easier to inspect and test. A model can be evaluated later against clearly defined scenarios, without claiming clinical accuracy.

**Q: Is this real student data?**
A: No. All supplied records are synthetic. No personal student information is included.

**Q: Why is hardware not integrated yet?**
A: We prioritised the core software flow. Hardware is a later extension and the environmental sensor will not be treated as a direct measure of wellbeing.
