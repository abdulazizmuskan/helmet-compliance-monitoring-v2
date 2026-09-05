import streamlit as st
import cv2
import numpy as np

from models.load_model import load_model
from database.db_operations import insert_detection
from utils.ui_components import (
    inject_global_css,
    render_sidebar_brand,
    render_sidebar_footer,
    render_header,
    render_result_card,
    section_header,
    empty_state,
)

st.set_page_config(page_title="Image Detection | Helmet Compliance", layout="wide")

inject_global_css()
render_sidebar_brand()
render_sidebar_footer(model_ready=True)

render_header(
    "Image Detection",
    "Upload a photo to run an instant helmet compliance check",
)

section_header("📤", "Upload Image")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if not uploaded_file:
    empty_state("🖼️", "Upload an image to begin analysis.")
else:
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if image is None:
        st.error("Unable to process the uploaded file.")
    else:
        with st.spinner("Running AI detection..."):
            try:
                model = load_model()
                results = model(image)

                class_id = results[0].probs.top1
                predicted_class = results[0].names[class_id]
                confidence = float(results[0].probs.top1conf)
            except Exception:
                st.error("Unable to process the uploaded file.")
                st.stop()

        # Persist this detection so Dashboard/Analytics reflect real activity
        insert_detection("image", predicted_class, confidence)

        section_header("🔍", "Detection Result")

        col1, col2 = st.columns(2)

        with col1:
            st.caption("ORIGINAL INPUT")
            st.image(
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                use_container_width=True,
            )

        with col2:
            st.caption("DETECTION STATUS")
            is_helmet = predicted_class.lower() == "helmet"

            render_result_card(
                is_safe=is_helmet,
                title="Helmet Detected" if is_helmet else "No Helmet Detected — Compliance Violation",
                subtitle=f"Predicted class: {predicted_class}  ·  Confidence: {confidence:.2%}",
            )

            st.markdown("<br/>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Predicted Class", predicted_class)
            with m2:
                st.metric("Confidence", f"{confidence:.2%}")

        st.success("Detection completed successfully")
