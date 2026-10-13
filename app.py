"""MindCheck Week 1 prototype: synthetic data + transparent trend dashboard."""
from __future__ import annotations
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from mindcheck.analysis import analyze_student

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "synthetic_checkins.csv"

st.set_page_config(page_title="MindCheck | Week 1 Prototype", page_icon="🧠", layout="wide")
st.title("🧠 MindCheck")
st.subheader("AI-assisted student wellbeing trend demonstration")
st.warning(
    "Prototype only: the dataset is synthetic and the thresholds are illustrative, not clinically validated. "
    "This tool does not diagnose burnout or any mental-health condition."
)

if not DATA_PATH.exists():
    st.error("Synthetic dataset not found. From the project folder, run: python generate_data.py")
    st.stop()

@st.cache_data
def load_data(path: str, mtime: float) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["date"])

data = load_data(str(DATA_PATH), DATA_PATH.stat().st_mtime)

with st.sidebar:
    st.header("Demo controls")
    st.caption("Select one synthetic profile to explore how baseline comparison works.")
    student_ids = sorted(data["student_id"].dropna().unique().tolist())
    selected_student = st.selectbox("Synthetic student", student_ids, index=0)
    st.divider()
    st.markdown("**Comparison method**")
    st.write("Baseline: first 7 observations")
    st.write("Recent window: latest 3 observations")
    st.write("Flag: at least 2 indicators cross their demo thresholds")
    st.caption("Workload is shown as a contextual self-report, not proof of burnout.")

student = data.loc[data["student_id"] == selected_student].sort_values("date").copy()
result = analyze_student(student)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Synthetic check-ins", f"{len(data):,}")
k2.metric("Synthetic profiles", f"{data['student_id'].nunique()}")
k3.metric("Selected profile records", f"{len(student)}")
k4.metric("Indicators over threshold", str(result.get("flagged_count", 0)))

st.markdown("### 1. Selected student's reported trends")
left, right = st.columns(2)
with left:
    fig = px.line(student, x="date", y=["stress", "mood", "fatigue"], markers=True,
                  title="Mood, stress and fatigue (self-reported)",
                  labels={"date": "Date", "value": "Score (scale 0–10)", "variable": "Measure"})
    fig.update_layout(legend_title_text="Measure", margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.line(student, x="date", y=["sleep_hours", "workload_hours"], markers=True,
                  title="Sleep and workload (self-reported)",
                  labels={"date": "Date", "value": "Hours per day", "variable": "Measure"})
    fig.update_layout(legend_title_text="Measure", margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 2. Transparent baseline comparison")
if result.get("ready"):
    st.write(f"**Baseline window:** {result['baseline_start']} to {result['baseline_end']} ({result['baseline_n']} observations)")
    st.write(f"**Recent window:** {result['recent_start']} to {result['recent_end']} ({result['recent_n']} observations)")
    st.info(f"**Result:** {result['status']}\n\n{result['summary']}")
    signals = pd.DataFrame(result["signals"])
    display = signals[["indicator", "baseline_mean", "recent_mean", "change", "threshold", "unit", "triggered", "interpretation"]].copy()
    display.rename(columns={
        "indicator": "Indicator", "baseline_mean": "Baseline mean", "recent_mean": "Recent mean",
        "change": "Raw change (recent − baseline)", "threshold": "Demo threshold",
        "unit": "Unit", "triggered": "Threshold crossed?", "interpretation": "Explanation"
    }, inplace=True)
    for col in ["Baseline mean", "Recent mean", "Raw change (recent − baseline)"]:
        display[col] = display[col].map(lambda value: "—" if pd.isna(value) or value is None else f"{value:+.2f}" if col == "Raw change (recent − baseline)" else f"{value:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)
else:
    st.info(result["summary"])

st.markdown("### 3. Download demo evidence")
col_a, col_b = st.columns(2)
with col_a:
    st.download_button("Download selected profile CSV", data=student.to_csv(index=False).encode("utf-8"),
                       file_name=f"{selected_student}_synthetic_checkins.csv", mime="text/csv")
with col_b:
    if result.get("ready"):
        report = pd.DataFrame(result["signals"])
        st.download_button("Download comparison table CSV", data=report.to_csv(index=False).encode("utf-8"),
                           file_name=f"{selected_student}_baseline_comparison.csv", mime="text/csv")

with st.expander("How the demo rules work"):
    st.markdown(
        "- Compute each indicator's mean over the first **7 observations** (baseline).\n"
        "- Compute its mean over the latest **3 observations** (recent window).\n"
        "- Example thresholds: stress rises by ≥2 points; sleep drops by ≥1.5 hours; mood drops by ≥1 point; fatigue rises by ≥2 points; workload rises by ≥2 hours/day.\n"
        "- The dashboard marks individual threshold crossings. Multiple crossings are a prompt to review a trend, not a diagnosis or a clinical risk score.\n\n"
        "These are engineering thresholds for a classroom prototype. They require literature review and expert/faculty input before any real-world wellbeing use."
    )

st.caption("MindCheck MDP · Week 1 proof of concept · Synthetic data only · Hardware intentionally deferred")
