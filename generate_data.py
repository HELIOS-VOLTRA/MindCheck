"""Generate a deterministic synthetic-only dataset for the MindCheck demo."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
START_DATE = pd.Timestamp("2026-09-01")
DAYS = 30


def clip(value: float, low: float, high: float) -> float:
    return float(np.clip(value, low, high))


def generate() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(20261009)
    rows: list[dict] = []
    labels: list[dict] = []

    scenarios = (
        ["stable"] * 8
        + ["gradual_stress_change"] * 8
        + ["sleep_disruption"] * 7
        + ["isolated_spike"] * 7
    )

    for index, scenario in enumerate(scenarios, start=1):
        student_id = f"S{index:03d}"
        # Student-specific starting points, generated solely for demonstration.
        base_stress = rng.normal(4.0, 0.55)
        base_mood = rng.normal(6.8, 0.45)
        base_sleep = rng.normal(7.3, 0.30)
        base_workload = rng.normal(4.2, 0.45)
        base_fatigue = rng.normal(4.0, 0.5)

        for day in range(DAYS):
            stress_shift = mood_shift = sleep_shift = workload_shift = fatigue_shift = 0.0

            if scenario == "gradual_stress_change" and day >= 12:
                progress = (day - 11) / (DAYS - 12)  # 0..1 over the change period
                stress_shift = 3.1 * progress
                mood_shift = -1.25 * progress
                fatigue_shift = 2.45 * progress
                workload_shift = 1.3 * progress
            elif scenario == "sleep_disruption" and day >= 18:
                progress = (day - 17) / (DAYS - 18)
                sleep_shift = -2.6 * progress
                fatigue_shift = 3.0 * progress
                mood_shift = -1.1 * progress
            elif scenario == "isolated_spike" and day == DAYS - 1:
                # One unusual stress report only; the 3-day average should resist overreacting.
                stress_shift = 4.2

            mood = clip(base_mood + mood_shift + rng.normal(0, 0.28), 1, 10)
            stress = clip(base_stress + stress_shift + rng.normal(0, 0.32), 0, 10)
            sleep = clip(base_sleep + sleep_shift + rng.normal(0, 0.25), 0, 12)
            workload = clip(base_workload + workload_shift + rng.normal(0, 0.30), 0, 16)
            fatigue = clip(base_fatigue + fatigue_shift + rng.normal(0, 0.35), 0, 10)

            rows.append({
                "student_id": student_id,
                "date": (START_DATE + pd.Timedelta(days=day)).date().isoformat(),
                "mood": round(mood, 1),
                "stress": round(stress, 1),
                "sleep_hours": round(sleep, 1),
                "workload_hours": round(workload, 1),
                "fatigue": round(fatigue, 1),
            })

        expected = {
            "stable": "No persistent multi-indicator change intended",
            "gradual_stress_change": "Persistent multi-indicator change intended",
            "sleep_disruption": "Persistent sleep/fatigue change intended",
            "isolated_spike": "Single-day stress spike; avoid overreacting",
        }[scenario]
        labels.append({"student_id": student_id, "scenario_type": scenario, "expected_pattern": expected})

    return pd.DataFrame(rows), pd.DataFrame(labels)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    checkins, evaluation_labels = generate()
    checkins.to_csv(DATA_DIR / "synthetic_checkins.csv", index=False)
    evaluation_labels.to_csv(DATA_DIR / "evaluation_labels.csv", index=False)
    print(f"Generated {len(checkins)} synthetic check-ins for {checkins['student_id'].nunique()} synthetic students.")
    print(f"Demo data: {DATA_DIR / 'synthetic_checkins.csv'}")
    print(f"Evaluation-only labels (not used by dashboard): {DATA_DIR / 'evaluation_labels.csv'}")


if __name__ == "__main__":
    main()
