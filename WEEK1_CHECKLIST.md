# Week 1 Checklist — MindCheck

**Week 1 target:** show a small working software proof-of-concept. Hardware is deliberately postponed.

## Day 1 — Set up the project
- [ ] Download/extract the starter kit.
- [ ] Install Python and project dependencies.
- [ ] Launch Streamlit locally.
- [ ] Each teammate gets the app running on one laptop if possible.

**Evidence:** screenshot of the running dashboard and terminal showing the local URL.

## Day 2 — Understand the data
- [ ] Open `data/synthetic_checkins.csv` in Excel or Python.
- [ ] Confirm 30 synthetic student IDs and 30 dates per student.
- [ ] Review the feature definitions: mood, stress, sleep, workload, fatigue.
- [ ] Keep `evaluation_labels.csv` separate from analysis inputs.

**Evidence:** dataset row count and a screenshot of a few synthetic rows.

## Day 3 — Understand the rules
- [ ] Read `mindcheck/analysis.py` together.
- [ ] Explain baseline = first 7 observations and recent = latest 3.
- [ ] Trace one indicator calculation by hand.
- [ ] Explain why one isolated spike should not automatically become a multi-indicator flag.

**Evidence:** one example calculation in your notes.

## Day 4 — Test the dashboard
- [ ] Switch through at least 4 synthetic profiles.
- [ ] Confirm chart values change when the selected ID changes.
- [ ] Inspect one stable profile and one changing profile.
- [ ] Test both CSV download buttons.

**Evidence:** 2–3 screenshots and downloaded CSV files.

## Day 5 — Run tests and improve small issues
- [ ] Run `python -m pytest -q`.
- [ ] Fix setup or data-loading problems.
- [ ] Do not add new complex features until these basics work.

**Evidence:** terminal screenshot of the test results.

## Day 6 — Prepare the panel demo
- [ ] Follow `DEMO_SCRIPT.md` and rehearse a 3–4 minute demonstration.
- [ ] Explain what is synthetic, how the rule works, and what is not yet validated.
- [ ] Capture one screenshot of trends and one of the comparison table.
- [ ] Prepare a one-slide architecture diagram: Synthetic check-ins → data processing → baseline rules → dashboard.

**Evidence:** a short demo recording or screenshots, if permitted by your guide.

## Day 7 — Freeze the Week 1 version
- [ ] Test the app from a fresh terminal using the README.
- [ ] Keep a backup ZIP of the exact working version.
- [ ] Write down known limitations and next steps.
- [ ] Ensure every team member can explain the prototype.

**Week 1 completion criteria:** app runs, synthetic data loads, graphs work, baseline comparison is visible, downloads work, tests pass, and the team can explain the limitations.

## Suggested ownership

| Teammate | Week 1 ownership |
|---|---|
| Sahithi K — AI & Robotics | Data and rule-engine walkthrough; verify synthetic scenarios |
| Rishab Kumar — AI & Robotics | Run/debug dashboard; charts and download checks |
| Aditya Bimal — Cybersecurity | Data minimisation, privacy wording and risk/limitations checklist |
| Thanika — Electronics & Computer Engineering | Setup/readme verification, data flow/architecture diagram, app reliability |

Everyone should test the complete flow. This division is a starting point, not a reason for only one person to understand a component.
