import streamlit as st
import os
import time
import librosa
import plotly.graph_objects as go
import streamlit.components.v1 as components

from api.client import predict_audio
from components.sidebar import render_sidebar
from components.gauge import render_gauge
from components.prediction_card import prediction_card
from components.explanation import render_explanation
from components.spectrogram import render_spectrogram, generate_spectrogram_file
from components.pdf_report import generate_pdf_report


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Deepfake Audio Detector",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SPLASH SCREEN
# =========================
if "intro_shown" not in st.session_state:
    st.session_state.intro_shown = False


def show_intro():
    if not st.session_state.intro_shown:
        splash_html = """
        <div style="text-align:center; padding-top:200px;">
            <h1 style="color:#00ffff; font-size:50px;">
                Initializing AI Detection Engine...
            </h1>
        </div>
        """
        components.html(splash_html, height=600)
        time.sleep(2)
        st.session_state.intro_shown = True
        st.rerun()


show_intro()

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# SIDEBAR
# =========================
page = render_sidebar()

# =========================
# DETECTION PAGE
# =========================
if page == "Detection":

    st.markdown("# 🎙️ AI Deepfake Audio Detection Dashboard")

    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=["wav", "mp3", "flac", "ogg"]
    )

    if uploaded_file:

        st.audio(uploaded_file)

        # Waveform
        try:
            y, sr = librosa.load(uploaded_file, sr=None)
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=y, mode="lines"))
            fig.update_layout(title="Audio Waveform", height=250)
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Could not render waveform")

        # Spectrogram
        render_spectrogram(uploaded_file)

        if st.button("Analyze Audio", use_container_width=True):

            with st.spinner("Running AI deepfake detection..."):
                start = time.time()
                result = predict_audio(uploaded_file)
                latency = time.time() - start

            if "error" in result:
                st.error(result["error"])
            else:
                prediction = result["prediction"]
                confidence = result["confidence"]

                # -------------------------
                # FRONTEND RISK POLICY
                # -------------------------
                percent = confidence * 100

                if percent <= 30:
                    decision = "ALLOW"
                elif percent <= 70:
                    decision = "CHALLENGE"
                else:
                    decision = "BLOCK"

                col1, col2 = st.columns(2)

                with col1:
                    prediction_card(prediction, confidence, decision)
                    render_explanation(confidence, decision)
                    st.info(f"Inference Time: {latency:.3f}s")

                with col2:
                    render_gauge(confidence)

                # Generate PDF
                spectrogram_path = generate_spectrogram_file(uploaded_file)

                pdf_path = generate_pdf_report(
                    uploaded_file.name,
                    prediction,
                    confidence,
                    decision,
                    latency,
                    spectrogram_path
                )

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download Report",
                        f,
                        file_name="deepfake_report.pdf",
                        use_container_width=True
                    )

                # Save history
                st.session_state.history.append({
                    "file": uploaded_file.name,
                    "confidence": confidence,
                    "decision": decision
                })

# =========================
# HISTORY PAGE
# =========================
elif page == "History":

    st.title("Detection History")

    if not st.session_state.history:
        st.info("No detections yet")
    else:
        for item in reversed(st.session_state.history):
            st.write(
                f"{item['file']} → {item['decision']} ({item['confidence']*100:.2f}%)"
            )

# =========================
# SYSTEM STATUS PAGE
# =========================
elif page == "System Status":

    st.title("System Status")

    st.success("Frontend Operational")
    st.info("Model: Hybrid CNN + Transformer")
    st.info("Risk Policy: 3-Level (Allow / Challenge / Block)")