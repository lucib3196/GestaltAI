import streamlit as st
from app.streamlit_app.services.llm_service import initialize_thread_id
from pydantic import BaseModel
from typing import Any, List
from app.streamlit_app.config import CHAT_NAMES


class DefaultState(BaseModel):
    messages: List[Any] = []
    thread_id: str
    chat_select: CHAT_NAMES | None


DEFAULT_STATE = DefaultState(
    messages=[], thread_id=initialize_thread_id(), chat_select=None
)


def init_session():
    for key, value in DEFAULT_STATE.model_dump().items():
        if key not in st.session_state:
            st.session_state[key] = value
