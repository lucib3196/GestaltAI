import streamlit as st
from app.streamlit_app.services.llm_service import initialize_thread_id
from chat_modes import CHAT_OPTIONS

DEFAULT_STATE = {
    "messages": [],
    "thread_id": initialize_thread_id(),
    "chat_select": CHAT_OPTIONS["file_generator"],
}


def init_session():
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value
