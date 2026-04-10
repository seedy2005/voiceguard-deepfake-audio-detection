import streamlit as st


def render_explanation(confidence, decision):

    # Ensure confidence is numeric
    try:
        percent = float(confidence)
    except:
        percent = 0.0

    # Convert to percentage if model returned 0–1
    if percent <= 1:
        percent *= 100

    # Risk styling
    if decision == "ALLOW":
        color = "#00ff99"
        risk_text = "LOW RISK"

    elif decision == "CHALLENGE":
        color = "#ffcc00"
        risk_text = "MEDIUM RISK"

    else:
        color = "#ff4b4b"
        risk_text = "HIGH RISK"

    # Render explanation card
    st.markdown(
        f"""
        <div style="
            background-color:#111;
            padding:22px;
            border-radius:14px;
            border:2px solid {color};
            box-shadow: 0 0 20px {color}55;
        ">

        <h3 style="color:{color}; margin-bottom:10px;">
            AI Decision Explanation
        </h3>

        <p style="font-size:16px;">
            <b>Confidence:</b> {percent:.2f}%
        </p>

        <p style="font-size:16px;">
            <b>Risk Level:</b>
            <span style="color:{color}; font-weight:bold;">
                {risk_text}
            </span>
        </p>

        <hr style="border-color:{color}; opacity:0.4;">

        <p style="font-size:15px; line-height:1.6;">
            The system analyzed spectral and temporal characteristics of the audio.
            Based on spoof probability thresholds, this sample falls under
            <b style="color:{color};">{decision}</b> category.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )