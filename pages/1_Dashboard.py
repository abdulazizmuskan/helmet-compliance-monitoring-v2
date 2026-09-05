import streamlit as st

from database.db_operations import get_summary_stats
from utils.ui_components import (
    inject_global_css,
    render_sidebar_brand,
    render_sidebar_footer,
    render_header,
    render_kpi_card,
    section_header,
    empty_state,
)

st.set_page_config(page_title="Dashboard | Helmet Compliance", layout="wide")

inject_global_css()
render_sidebar_brand()
render_sidebar_footer(model_ready=True)

render_header(
    "Compliance Dashboard",
    "Real-time helmet compliance monitoring, powered by AI",
)

stats = get_summary_stats()

if stats["total"] == 0:
    empty_state(
        "📊",
        "No detections recorded yet. Run an Image or Video detection to populate this dashboard.",
    )
else:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(
            "👷", "Total Detections", f"{stats['total']:,}",
            "All recorded checks", accent="info",
        )
    with col2:
        render_kpi_card(
            "✅", "Helmet Compliant", f"{stats['compliant']:,}",
            "Passed compliance check", accent="safe",
        )
    with col3:
        render_kpi_card(
            "⚠️", "Violations", f"{stats['violations']:,}",
            "No helmet detected", accent="violation",
        )
    with col4:
        render_kpi_card(
            "📈", "Compliance Rate", f"{stats['compliance_rate']:.1f}%",
            "Compliant / total detections", accent="warning",
        )

st.markdown("<br/>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    section_header("🚀", "Project Overview")
    st.markdown(
        """
        <div class="kpi-card">
        This system uses a custom-trained YOLO classification model to:

        - Detect Helmet / No Helmet
        - Monitor safety compliance
        - Process images and videos
        - Generate safety analytics

        Built with Python, Streamlit, OpenCV, and YOLO.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    section_header("🩺", "System Status")
    st.markdown(
        """
        <div class="kpi-card" style="line-height: 2;">
            <span class="badge safe">● Dashboard Online</span><br/>
            <span class="badge safe">● Image Detection Ready</span><br/>
            <span class="badge safe">● Video Detection Ready</span><br/>
            <span class="badge safe">● Analytics Active</span><br/>
            <span class="badge info">● Model Loaded</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_header("📋", "Safety Recommendations")

st.markdown(
    """
    <div class="kpi-card" style="margin-bottom:0.6rem;">⚠️ Workers entering a construction site must wear helmets at all times.</div>
    <div class="kpi-card" style="margin-bottom:0.6rem;">⚠️ Regular compliance checks should be conducted using AI-assisted monitoring.</div>
    <div class="kpi-card">⚠️ Violations should be reported immediately to safety supervisors.</div>
    """,
    unsafe_allow_html=True,
)
