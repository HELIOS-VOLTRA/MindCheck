"""Transparent, non-clinical baseline trend rules for the MindCheck prototype.

These thresholds are demonstration engineering choices, not validated clinical
cut-offs. The output describes changes in self-reported data; it does not
estimate or diagnose a mental-health condition.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

DATE_COL = "date"
MIN_TOTAL_ROWS = 10
BASELINE_DAYS = 7
RECENT_DAYS = 3
MIN_VALID_BASELINE = 5
MIN_VALID_RECENT = 2


@dataclass(frozen=True)
class IndicatorRule:
    label: str
    column: str
    direction: str  # "increase" means recent - baseline; "decrease" means baseline - recent
    threshold: float
    unit: str
    explanation: str


RULES = (
    IndicatorRule("Stress", "stress", "increase", 2.0, "points / 10", "Recent reported stress is higher than baseline."),
    IndicatorRule("Sleep duration", "sleep_hours", "decrease", 1.5, "hours / night", "Recent reported sleep duration is lower than baseline."),
    IndicatorRule("Mood", "mood", "decrease", 1.0, "points / 10", "Recent reported mood is lower than baseline."),
    IndicatorRule("Fatigue", "fatigue", "increase", 2.0, "points / 10", "Recent reported fatigue is higher than baseline."),
    IndicatorRule("Workload", "workload_hours", "increase", 2.0, "hours / day", "Recent reported workload is higher than baseline."),
)

REQUIRED_COLUMNS = {DATE_COL, "mood", "stress", "sleep_hours", "workload_hours", "fatigue"}


def _mean(series: pd.Series) -> float | None:
    valid = pd.to_numeric(series, errors="coerce").dropna()
    if valid.empty:
        return None
    return float(valid.mean())


def analyze_student(student_df: pd.DataFrame) -> dict[str, Any]:
    """Compare a student's first 7 available observations with the latest 3.

    The caller should pass data for one student. Minimum valid-day checks are
    applied to avoid producing a result from too little data.
    """
    missing = sorted(REQUIRED_COLUMNS - set(student_df.columns))
    if missing:
        return {
            "ready": False,
            "status": "Data columns missing",
            "summary": f"The dataset is missing required columns: {', '.join(missing)}.",
            "signals": [],
            "flagged_count": 0,
        }

    data = student_df.copy()
    data[DATE_COL] = pd.to_datetime(data[DATE_COL], errors="coerce")
    data = data.dropna(subset=[DATE_COL]).sort_values(DATE_COL)

    if len(data) < MIN_TOTAL_ROWS:
        return {
            "ready": False,
            "status": "More check-ins needed",
            "summary": f"At least {MIN_TOTAL_ROWS} dated observations are needed for this demo comparison.",
            "signals": [],
            "flagged_count": 0,
        }

    baseline = data.iloc[:BASELINE_DAYS]
    recent = data.iloc[-RECENT_DAYS:]
    signals: list[dict[str, Any]] = []

    for rule in RULES:
        baseline_mean = _mean(baseline[rule.column])
        recent_mean = _mean(recent[rule.column])
        baseline_count = int(pd.to_numeric(baseline[rule.column], errors="coerce").notna().sum())
        recent_count = int(pd.to_numeric(recent[rule.column], errors="coerce").notna().sum())

        enough_data = baseline_count >= MIN_VALID_BASELINE and recent_count >= MIN_VALID_RECENT
        raw_delta = None if baseline_mean is None or recent_mean is None else recent_mean - baseline_mean
        if raw_delta is None:
            directional_change = None
        elif rule.direction == "increase":
            directional_change = raw_delta
        else:
            directional_change = -raw_delta

        triggered = bool(
            enough_data
            and directional_change is not None
            and directional_change >= rule.threshold
        )
        signals.append({
            "indicator": rule.label,
            "baseline_mean": baseline_mean,
            "recent_mean": recent_mean,
            "change": raw_delta,
            "change_direction": rule.direction,
            "threshold": rule.threshold,
            "unit": rule.unit,
            "triggered": triggered,
            "enough_data": enough_data,
            "interpretation": rule.explanation if triggered else "No demo threshold crossing for this indicator.",
        })

    flagged_count = sum(1 for signal in signals if signal["triggered"])
    if any(not signal["enough_data"] for signal in signals):
        # Continue showing valid calculations, but tell the viewer data quality is limited.
        status = "Limited data for some indicators"
        summary = "Some indicators have too few valid observations; interpret the comparison cautiously."
    elif flagged_count >= 2:
        status = "Multiple changes above demo thresholds"
        summary = f"{flagged_count} indicators crossed the prototype's demonstration thresholds. Review the trends; this is not a diagnosis."
    elif flagged_count == 1:
        status = "One change above a demo threshold"
        summary = "One indicator crossed a demonstration threshold. Review the context and future check-ins; this is not a diagnosis."
    else:
        status = "No demo threshold crossings"
        summary = "No indicator crossed the selected demonstration thresholds in this comparison. This does not prove that a student is well."

    return {
        "ready": True,
        "status": status,
        "summary": summary,
        "flagged_count": int(flagged_count),
        "signals": signals,
        "baseline_start": baseline[DATE_COL].min().date().isoformat(),
        "baseline_end": baseline[DATE_COL].max().date().isoformat(),
        "recent_start": recent[DATE_COL].min().date().isoformat(),
        "recent_end": recent[DATE_COL].max().date().isoformat(),
        "baseline_n": int(len(baseline)),
        "recent_n": int(len(recent)),
    }
