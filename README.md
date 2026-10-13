# MindCheck — Week 1 Starter Kit

A small, runnable proof-of-concept for the MindCheck MDP. It demonstrates:

- synthetic (fake) student check-in data;
- transparent comparison of a student's first 7 observations against the latest 3;
- a Streamlit dashboard with trend charts and indicator explanations;
- a small test suite for the core rule engine.

**Hardware is intentionally deferred.** This week's goal is to get the software demo running end-to-end first.

## Important boundary

This is an educational prototype, not a clinical screening tool. All included student records are synthetic. Thresholds are illustrative engineering choices and have not been clinically validated. The app does not diagnose burnout or any mental-health condition. Do not enter real or identifiable student data into this demo.

## 1. What is included?

```text
MindCheck_Week1_Starter/
├── app.py                         # Streamlit dashboard
├── generate_data.py               # Rebuilds the synthetic dataset
├── requirements.txt               # Python dependencies
├── mindcheck/
│   ├── __init__.py
│   └── analysis.py                # Transparent baseline rule engine
├── data/
│   ├── synthetic_checkins.csv     # 900 fake check-ins, ready to use
│   └── evaluation_labels.csv      # Scenario labels for evaluation only
├── tests/
│   └── test_analysis.py           # Core logic tests
├── WEEK1_CHECKLIST.md              # Day-by-day team plan
├── DEMO_SCRIPT.md                  # Suggested panel demo narration
└── LIMITATIONS_AND_TEST_PLAN.md    # What to test and what not to claim
```

The dashboard reads `synthetic_checkins.csv`. It does **not** load `evaluation_labels.csv`. Keep the evaluation labels separate from the analysis input; they describe how the synthetic scenarios were generated and are not features for the rule engine.

## 2. Run it on Windows

Install Python 3.11 or 3.12 if it is not already installed. During installation, select **Add Python to PATH**.

1. Extract the ZIP file.
2. Open the extracted `MindCheck_Week1_Starter` folder.
3. Click the folder address bar in File Explorer, type `cmd`, and press Enter.
4. Create a virtual environment:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Start the dashboard:

```bat
python -m streamlit run app.py
```

Streamlit should open a browser tab. If it does not, open the local URL printed in the terminal (commonly `http://localhost:8501`). Keep that terminal open while using the app. Stop the server with `Ctrl+C`.

### If `py` is not recognised

Try `python --version`, then replace `py` with `python` in the commands above. If neither works, install Python and reopen Command Prompt.

## 3. Run it on macOS / Linux

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

## 4. Regenerate the synthetic data

From the project folder with the environment activated:

```bash
python generate_data.py
```

This creates:
- `data/synthetic_checkins.csv`: 30 synthetic profiles × 30 daily records = 900 records;
- `data/evaluation_labels.csv`: a separate description of each synthetic scenario.

The synthetic scenarios are stable patterns, gradual multi-indicator change, sleep disruption, and an isolated single-day stress spike. Their purpose is to exercise the demo logic, not to represent real students.

## 5. Run the tests

```bash
python -m pytest -q
```

Expected result: 4 passing tests. If dependencies are not installed, run the setup steps first.

## 6. How the prototype rule engine works

1. Sort a selected synthetic student's observations by date.
2. Calculate each indicator's mean over the first 7 observations (baseline).
3. Calculate the mean over the most recent 3 observations.
4. Check illustrative thresholds:
   - stress increase ≥ 2 points on a 0–10 scale;
   - sleep decrease ≥ 1.5 hours/night;
   - mood decrease ≥ 1 point on a 0–10 scale;
   - fatigue increase ≥ 2 points on a 0–10 scale;
   - workload increase ≥ 2 hours/day.
5. Show every indicator crossing in the dashboard. Two or more crossings are summarised as multiple changes above demonstration thresholds. Results are descriptive prompts to review the trend, not a diagnosis or clinical risk score.

These values are intentionally easy to inspect and change in `mindcheck/analysis.py`. They are not validated cut-offs. Before any use with real people, discuss the questionnaire, measures, consent, and interpretation with the project guide and relevant institutional experts.

## 7. Troubleshooting

- **`ModuleNotFoundError: streamlit`**: activate `.venv`, then run `pip install -r requirements.txt`.
- **Browser page is blank or unavailable**: check the terminal for errors and use the local URL printed by Streamlit.
- **Data not found**: confirm `data/synthetic_checkins.csv` exists; run `python generate_data.py` from the project root.
- **The dashboard says there is no threshold crossing**: try another synthetic profile in the sidebar. Not every synthetic profile should produce a flag.
- **Charts or scores look unexpected**: verify the selected profile and dates. Explain the comparison in the demo rather than presenting the result as a prediction.

## Suggested Week 1 definition of done

- [ ] App launches locally from the README instructions.
- [ ] Sidebar switches between synthetic profiles.
- [ ] Both time-series charts display.
- [ ] Baseline/recent windows and threshold table are visible.
- [ ] CSV downloads work.
- [ ] Core tests pass.
- [ ] Screenshots captured and demo rehearsed.
- [ ] Every team member can explain their contribution and the non-clinical limitations.
