import streamlit as st
import pandas as pd

from database.db_operations import get_recent_detections, get_summary_stats
from utils.ui_components import (
    inject_global_css,
    render_sidebar_brand,
    render_sidebar_footer,
    render_header,
    render_kpi_card,
    section_header,
    empty_state,
)

st.set_page_config(page_title="Analytics | Helmet Compliance", layout="wide")

inject_global_css()
render_sidebar_brand()
render_sidebar_footer(model_ready=True)

render_header(
    "Compliance Analytics",
    "Trends and breakdowns across all recorded detections",
)

rows = get_recent_detections(limit=1000)

if not rows:
    empty_state(
        "📈",
        "No detection history available yet. Run Image or Video detection to build analytics.",
    )
else:
    df = pd.DataFrame(
        rows,
        columns=["timestamp", "source_type", "predicted_class", "confidence", "is_compliant"],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    stats = get_summary_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("📊", "Total Records", f"{stats['total']:,}", accent="info")
    with col2:
        render_kpi_card("✅", "Compliance Rate", f"{stats['compliance_rate']:.1f}%", accent="safe")
    with col3:
        render_kpi_card("⚠️", "Violations Logged", f"{stats['violations']:,}", accent="violation")

    st.markdown("<br/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("📈", "Compliance Trend Over Time")
        daily = df.groupby("date")["is_compliant"].mean().mul(100).rename("Compliance %")
        st.line_chart(daily)

    with col2:
        section_header("🥧", "Compliant vs. Violation")
        counts = df["is_compliant"].map({1: "Compliant", 0: "Violation"}).value_counts()
        st.bar_chart(counts)

    section_header("🎯", "Confidence Distribution")
    st.bar_chart(df["confidence"].round(1).value_counts().sort_index())

    section_header("🗂️", "Detection Source Breakdown")
    source_counts = df["source_type"].value_counts()
    st.bar_chart(source_counts)

    section_header("📋", "Recent Detections")
    display_df = df[["timestamp", "source_type", "predicted_class", "confidence", "is_compliant"]].copy()
    display_df["confidence"] = (display_df["confidence"] * 100).round(1).astype(str) + "%"
    display_df["is_compliant"] = display_df["is_compliant"].map({1: "Compliant", 0: "Violation"})
    display_df.columns = ["Timestamp", "Source", "Predicted Class", "Confidence", "Status"]
    st.dataframe(display_df.head(50), use_container_width=True, hide_index=True)
