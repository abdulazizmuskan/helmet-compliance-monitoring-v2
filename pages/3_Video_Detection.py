import streamlit as st
import tempfile
import cv2

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

st.set_page_config(page_title="Video Detection | Helmet Compliance", layout="wide")

inject_global_css()
render_sidebar_brand()
render_sidebar_footer(model_ready=True)

render_header(
    "Video Detection",
    "Process a video frame-by-frame for helmet compliance",
)

# Log at most this many frames per video to the database, so a long video
# doesn't flood the detections table with thousands of near-duplicate rows.
LOG_EVERY_N_FRAMES = 15

section_header("📤", "Upload Video")

video_file = st.file_uploader(
    "Upload a Video",
    type=["mp4", "avi", "mov"],
    label_visibility="collapsed",
)

if not video_file:
    empty_state("🎥", "Upload a video to begin analysis.")
else:
    try:
        model = load_model()
    except Exception:
        st.error("Unable to process the uploaded file.")
        st.stop()

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())

    cap = cv2.VideoCapture(temp_file.name)

    if not cap.isOpened():
        st.error("Unable to process the uploaded file.")
        st.stop()

    section_header("🔍", "Live Processing")

    col1, col2 = st.columns([2, 1])

    with col1:
        frame_placeholder = st.empty()
    with col2:
        stat_placeholder = st.empty()
        result_placeholder = st.empty()

    frame_count = 0
    compliant_frames = 0
    violation_frames = 0

    with st.spinner("Running AI detection..."):
        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            results = model(frame)

            class_id = results[0].probs.top1
            predicted_class = results[0].names[class_id]
            confidence = float(results[0].probs.top1conf)

            is_helmet = predicted_class.lower() == "helmet"
            if is_helmet:
                compliant_frames += 1
            else:
                violation_frames += 1

            frame_count += 1

            if frame_count % LOG_EVERY_N_FRAMES == 0:
                insert_detection("video", predicted_class, confidence)

            display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(display_frame, use_container_width=True)

            live_rate = (compliant_frames / frame_count * 100) if frame_count else 0
            stat_placeholder.markdown(
                f"""
                <div class="kpi-card" style="margin-bottom:0.7rem;">
                    <div class="kpi-label">Frames Processed</div>
                    <div class="kpi-value" style="font-size:1.4rem;">{frame_count}</div>
                </div>
                <div class="kpi-card" style="margin-bottom:0.7rem;">
                    <div class="kpi-label">Live Compliance Rate</div>
                    <div class="kpi-value" style="font-size:1.4rem;">{live_rate:.1f}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Violations</div>
                    <div class="kpi-value" style="font-size:1.4rem; color:#EF4444;">{violation_frames}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with result_placeholder.container():
                render_result_card(
                    is_safe=is_helmet,
                    title="Helmet Detected" if is_helmet else "No Helmet Detected",
                    subtitle=f"Confidence: {confidence:.2%}",
                )

    cap.release()

    # Log a final aggregate row so a very short video (fewer than
    # LOG_EVERY_N_FRAMES frames) still contributes at least one record.
    if frame_count > 0 and frame_count < LOG_EVERY_N_FRAMES:
        insert_detection("video", predicted_class, confidence)

    st.success("Video processing completed")
