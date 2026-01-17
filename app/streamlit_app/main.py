import streamlit as st
from core.settings import get_settings
from pathlib import Path
from streamlit_app.ui.layout import (
    render_sidebar,
    render_title,
    render_chatbot_description,
    render_downloads,
)
from streamlit_app.state.session import init_session
from streamlit_app.pages import chat

settings = get_settings()


init_session()
OUTPUT_DIR = Path(settings.output_path).resolve()
OUTPUT_DIR.mkdir(exist_ok=True)


def render_ui():
    # Header Section
    render_title(settings.environment, thread_id=st.session_state.thread_id)
    render_sidebar()
    render_chatbot_description()

    # Actual Chat Component
    chat.render_chat()
    chat.render_chat_input()

    # Render downloads if they exist
    render_downloads(OUTPUT_DIR)


render_ui()
