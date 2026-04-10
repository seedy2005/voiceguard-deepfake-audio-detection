import streamlit as st
import plotly.graph_objects as go
import time


def generate_gradient_steps():

    steps = []

    # Create 100 tiny gradient segments
    for i in range(100):
        if i < 50:
            # Green → Yellow
            r = int(255 * (i / 50))
            g = 255
            b = 0
        else:
            # Yellow → Red
            r = 255
            g = int(255 * (1 - (i - 50) / 50))
            b = 0

        color = f"rgb({r},{g},{b})"

        steps.append({
            "range": [i, i + 1],
            "color": color
        })

    return steps


def render_gauge(confidence):

    try:
        confidence = float(confidence)
    except:
        confidence = 0.0

    final_value = confidence * 100

    # Risk logic
    if final_value <= 30:
        glow_color = "#00ff99"
        blink_speed = None
    elif final_value <= 70:
        glow_color = "#ffcc00"
        blink_speed = 1.5
    else:
        glow_color = "#ff0033"
        blink_speed = 0.6

    gradient_steps = generate_gradient_steps()

    placeholder = st.empty()

    # Smooth animation sweep
    for value in range(0, int(final_value) + 1, 2):

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 60, "color": glow_color}},
            title={"text": "Spoof Probability (%)"},
            gauge={
                "shape": "angular",
                "axis": {"range": [0, 100]},
                "bar": {"color": glow_color},
                "steps": gradient_steps,
                "threshold": {
                    "line": {"color": glow_color, "width": 6},
                    "thickness": 0.75,
                    "value": value
                }
            }
        ))

        fig.update_layout(
            height=500,
            margin=dict(l=40, r=40, t=80, b=40),
            paper_bgcolor="#0d0d0d",
            font={"color": glow_color}
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.015)

    # Neon glow
    if blink_speed:
        st.markdown(
            f"""
            <style>
            @keyframes neonPulse {{
                0% {{ box-shadow: 0 0 15px {glow_color}; }}
                50% {{ box-shadow: 0 0 40px {glow_color}; }}
                100% {{ box-shadow: 0 0 15px {glow_color}; }}
            }}

            div[data-testid="stPlotlyChart"] {{
                border-radius: 25px;
                padding: 15px;
                animation: neonPulse {blink_speed}s infinite;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <style>
            div[data-testid="stPlotlyChart"] {{
                box-shadow: 0 0 30px {glow_color};
                border-radius: 25px;
                padding: 15px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )