import pandas as pd

from mindcheck.analysis import analyze_student


def make_student(stress_values=None, sleep_values=None, mood_values=None, fatigue_values=None, workload_values=None):
    n = 12
    stress_values = stress_values or [4.0] * n
    sleep_values = sleep_values or [7.0] * n
    mood_values = mood_values or [7.0] * n
    fatigue_values = fatigue_values or [4.0] * n
    workload_values = workload_values or [4.0] * n
    return pd.DataFrame({
        "date": pd.date_range("2026-09-01", periods=n),
        "mood": mood_values,
        "stress": stress_values,
        "sleep_hours": sleep_values,
        "workload_hours": workload_values,
        "fatigue": fatigue_values,
    })


def test_stable_profile_has_no_threshold_crossing():
    result = analyze_student(make_student())
    assert result["ready"] is True
    assert result["flagged_count"] == 0
    assert result["status"] == "No demo threshold crossings"


def test_two_persistent_indicator_changes_are_flagged():
    stress = [4.0] * 7 + [6.7] * 5
    sleep = [7.2] * 7 + [5.4] * 5
    result = analyze_student(make_student(stress_values=stress, sleep_values=sleep))
    assert result["flagged_count"] >= 2
    assert result["status"] == "Multiple changes above demo thresholds"


def test_single_indicator_crossing_is_not_multi_indicator_flag():
    stress = [4.0] * 7 + [6.5] * 5
    result = analyze_student(make_student(stress_values=stress))
    assert result["flagged_count"] == 1
    assert result["status"] == "One change above a demo threshold"


def test_too_few_observations_returns_not_ready():
    df = make_student().iloc[:8]
    result = analyze_student(df)
    assert result["ready"] is False
    assert result["status"] == "More check-ins needed"


def test_bundled_synthetic_scenarios_behave_as_designed():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    checkins = pd.read_csv(root / "data" / "synthetic_checkins.csv")
    labels = pd.read_csv(root / "data" / "evaluation_labels.csv")
    for _, row in labels.iterrows():
        result = analyze_student(checkins[checkins["student_id"] == row["student_id"]])
        if row["scenario_type"] in {"stable", "isolated_spike"}:
            assert result["flagged_count"] == 0
        elif row["scenario_type"] in {"gradual_stress_change", "sleep_disruption"}:
            assert result["flagged_count"] >= 2
