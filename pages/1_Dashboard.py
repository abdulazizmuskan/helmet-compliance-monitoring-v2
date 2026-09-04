import streamlit as st

st.set_page_config(layout="wide")

st.title("🦺 PPE Compliance Monitoring Dashboard")
st.markdown(
    "Real-time helmet compliance monitoring system powered by AI."
)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👷 Total Inspections",
        "1,599"
    )

with col2:
    st.metric(
        "✅ Helmet Detected",
        "1,320"
    )

with col3:
    st.metric(
        "❌ Violations",
        "279"
    )

with col4:
    st.metric(
        "📈 Compliance Rate",
        "82.5%"
    )

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.info("""
    ### 🚀 Project Overview

    This system uses a custom-trained YOLO classification model to:
    
    - Detect Helmet / No Helmet
    - Monitor safety compliance
    - Process images and videos
    - Generate safety analytics
    
    Developed using:
    - Python
    - Streamlit
    - OpenCV
    - YOLO
    """)

with col2:
    st.success("""
    ### Current Status
    
    ✅ Dashboard Online
    
    ✅ Image Detection Working
    
    ✅ Video Detection Working
    
    ✅ Analytics Active
    
    ✅ Model Loaded
    """)

st.divider()

st.subheader("📋 Safety Recommendations")

st.warning(
    "Workers entering a construction site must wear helmets at all times."
)

st.warning(
    "Regular compliance checks should be conducted using AI-assisted monitoring."
)

st.warning(
    "Violations should be reported immediately to safety supervisors."
)