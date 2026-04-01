import streamlit as st
from analysis.data_loader import load_data


def ensure_session_state():
    if "df" not in st.session_state:
        st.session_state["df"] = load_data()

    if "min_matches" not in st.session_state:
        st.session_state["min_matches"] = 15

    if "selected_seasons" not in st.session_state:
        st.session_state["selected_seasons"] = sorted(st.session_state["df"]["Season"].unique())
