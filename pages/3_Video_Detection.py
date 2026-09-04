import streamlit as st
import tempfile
import cv2

from models.load_model import load_model

st.title("🎥 Helmet Video Detection")

model = load_model()

video_file = st.file_uploader(
    "Upload a Video",
    type=["mp4", "avi", "mov"]
)

if video_file:

    temp_file = tempfile.NamedTemporaryFile(delete=False)

    temp_file.write(video_file.read())

    cap = cv2.VideoCapture(temp_file.name)

    frame_placeholder = st.empty()

    prediction_placeholder = st.empty()

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        class_id = results[0].probs.top1

        predicted_class = results[0].names[class_id]

        confidence = float(
            results[0].probs.top1conf
        )

        display_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            display_frame,
            use_container_width=True
        )

        if predicted_class == "helmet":

            prediction_placeholder.success(
                f"✅ Helmet Detected ({confidence:.2%})"
            )

        else:

            prediction_placeholder.error(
                f"❌ No Helmet Detected ({confidence:.2%})"
            )

    cap.release()

    st.success("Video Processing Completed")