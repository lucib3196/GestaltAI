import streamlit as st
from chat_modes import CHAT_OPTIONS
from settings import ENV


def render_title(env: ENV, thread_id: str | None = None):
    title = "Gestalt AI"
    if env == "local":
        title += " (Local DEV)"
    if thread_id:
        title += f" {thread_id}"

    st.set_page_config(page_title=title, layout="centered")
    st.title(title)


def render_sidebar() -> str | None:
    options = [v.label for v in CHAT_OPTIONS.values() if v.active]
    with st.sidebar:
        add_radio = st.radio(
            label="Choose Chat Mode", options=options, index=None, key="chat_sidebar"
        )

    return add_radio
