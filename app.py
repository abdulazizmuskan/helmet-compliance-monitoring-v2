import streamlit as st

from utils.ui_components import (
    inject_global_css,
    render_sidebar_brand,
    render_sidebar_footer,
    render_header,
    section_header,
)

st.set_page_config(
    page_title="Helmet Compliance Monitoring",
    page_icon="🛡️",
    layout="wide",
)

inject_global_css()
render_sidebar_brand()
render_sidebar_footer(model_ready=True)

render_header(
    "Helmet Compliance Monitoring",
    "AI-powered safety detection and compliance analytics",
)

section_header("🛡️", "Overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        This system uses a custom-trained YOLO classification model to
        monitor helmet compliance from uploaded images and video.

        **What you can do:**
        - **Dashboard** — live compliance KPIs pulled from every recorded detection
        - **Image Detection** — upload a photo and get an instant compliance check
        - **Video Detection** — process a video frame-by-frame for compliance
        - **Analytics** — trends and breakdowns across all detection history

        Use the sidebar to navigate between sections.
        """
    )

with col2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">Stack</div>
                <div class="kpi-icon">⚙️</div>
            </div>
            <div class="kpi-sub" style="margin-top:0.3rem; line-height:1.7;">
                Python &middot; Streamlit<br/>
                OpenCV &middot; YOLO (Ultralytics)<br/>
                SQLite
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
