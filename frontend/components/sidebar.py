import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"


def check_backend():

    try:
        requests.get(BACKEND_URL, timeout=3)
        return True
    except:
        return False


def render_sidebar():

    with st.sidebar:

        st.markdown("## AI Detector")

        page = st.radio(

            "Navigation",

            [

                "Detection",

                "History",

                "System Status"

            ]

        )

        st.divider()

        if check_backend():

            st.success("Backend Online")

        else:

            st.error("Backend Offline")

        st.divider()

        st.caption("Model: CNN + Transformer")

        st.caption("Version: 1.0")

        st.caption("Frontend: Streamlit")

        return page