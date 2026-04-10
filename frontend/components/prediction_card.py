import streamlit as st

def prediction_card(prediction, confidence, decision):

    percent = confidence * 100

    # -------------------------
    # STYLE BASED ON DECISION
    # -------------------------

    if decision == "ALLOW":
        color = "#00ff99"
        display_text = f"Prediction: {prediction} ({percent:.2f}%)"

    elif decision == "CHALLENGE":
        color = "#ffcc00"  # Yellow
        display_text = f"Confidence: {percent:.2f}%"

    else:  # BLOCK
        color = "#ff4b4b"
        display_text = f"Prediction: FAKE ({percent:.2f}%)"

    st.markdown(
        f"""
        <div style="
            border: 2px solid {color};
            padding: 20px;
            border-radius: 12px;
            font-size: 26px;
            font-weight: bold;
            color: {color};
        ">
            {display_text}
            <br><br>
            Risk Level: {decision}
        </div>
        """,
        unsafe_allow_html=True
    )