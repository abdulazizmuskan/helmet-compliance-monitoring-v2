import streamlit as st
import pandas as pd

st.title("📈 Compliance Analytics")

data = pd.DataFrame({
    "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    "Compliance":[75,80,84,90,88,92,95]
})

st.subheader("Weekly Compliance Trend")

st.line_chart(
    data.set_index("Day")
)

st.subheader("Summary")

st.success(
    "Overall Compliance Improved by 20% This Week 🚀"
)