import streamlit as st
from ultralytics import YOLO


@st.cache_resource
def load_model():
    return YOLO("models/ppe_model.pt")