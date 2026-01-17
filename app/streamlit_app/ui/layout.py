import streamlit as st
from app.core.settings import ENV
from app.streamlit_app.chat_modes import (
    CHAT_OPTIONS,
    ChatOption,
)
from pathlib import Path


def render_title(env: ENV, thread_id: str | None = None):
    title = "Gestalt AI"
    if env == "local":
        title += " (Local DEV)"
    if thread_id:
        title += f" {thread_id}"

    st.set_page_config(page_title=title, layout="centered")
    st.title(title)


def render_sidebar() -> str | None:
    # Renders the labele for the option
    options = [k for k, v in CHAT_OPTIONS.items() if v.active]
    with st.sidebar:
        add_radio = st.radio(
            label="Choose Chat Mode",
            options=options,
            index=None,
            key="chat_select",
            format_func=lambda k: CHAT_OPTIONS[k].label,
            on_change=handle_chatbot_change,
        )

    return add_radio


def render_chatbot_description():
    if "chat_data" in st.session_state:
        chat_data: ChatOption = st.session_state.chat_data
        st.subheader(chat_data.label)
        st.write(chat_data.description)

        if chat_data.mode == "file":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                st.write(bytes_data)


def handle_chatbot_change():
    selected = st.session_state.chat_select
    if not selected:
        return
    chat_data = CHAT_OPTIONS[selected]
    st.session_state.chat_data = chat_data


def render_downloads(output_dir: Path, header: str = "Downloads") -> None:
    """
    Render download buttons for all files in a directory.

    If the directory contains no files, nothing is rendered.

    Args:
        output_dir (Path): Directory containing downloadable files.
        header (str): Optional section header label.
    """
    if not output_dir.exists():
        return

    files = [f for f in output_dir.iterdir() if f.is_file()]

    if not files:
        return

    st.divider()
    st.header(header)

    for file in files:
        with open(file, "rb") as f:
            st.download_button(
                label=f"Download {file.name}",
                data=f,
                file_name=file.name,
            )
