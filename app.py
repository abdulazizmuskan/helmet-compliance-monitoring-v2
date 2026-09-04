import streamlit as st

st.set_page_config(
    page_title="PPE Detection System",
    page_icon="🦺",
    layout="wide"
)

st.title("🦺 PPE Detection System")

st.markdown("""
Welcome to the PPE Detection System.

Use the sidebar to navigate:
- Dashboard
- Image Detection
- Video Detection
- Analytics
""")