import streamlit as st
import cv2
import numpy as np

from models.load_model import load_model

st.title("🦺 Helmet Detection")

model = load_model()

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    st.image(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        caption="Uploaded Image"
    )

    results = model(image)

    class_id = results[0].probs.top1

    predicted_class = results[0].names[class_id]

    confidence = float(
        results[0].probs.top1conf
    )

    st.subheader("Prediction")

    st.write(
        f"Class: {predicted_class}"
    )

    st.write(
        f"Confidence: {confidence:.2%}"
    )

    if predicted_class == "helmet":
        st.success("✅ Helmet Detected")

    else:
        st.error("❌ No Helmet Detected")