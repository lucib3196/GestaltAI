import streamlit as st
import os
from langgraph_sdk import get_client
from dotenv import load_dotenv
import asyncio
from typing import Literal
from config import OPTIONS, CHAT_NAMES, CHAT_OPTIONS, ChatOption


client = get_client(
    url="https://gestaltai-146ee200f93f5d6688814feed1edce29.us.langgraph.app",
    api_key=os.getenv("LANGSMITH_API_KEY"),
)

st.set_page_config(page_title="Gestalt AI", layout="centered")
st.title("Gestalt AI")


def handle_chatbot_change():
    selected = st.session_state.chat_select
    if not selected:
        return
    chat_data = CHAT_OPTIONS[selected]
    st.session_state.chat_data = chat_data


if "chat_data" in st.session_state:
    chat_data: ChatOption = st.session_state.chat_data

    st.subheader(chat_data.label)
    st.write(chat_data.description)

st.selectbox(
    label="Choose Chat",
    options=OPTIONS,
    index=None,
    key="chat_select",
    placeholder="Select Chat Mode...",
    on_change=handle_chatbot_change,
)

if "chat_data" in st.session_state:
    chat_data: ChatOption = st.session_state.chat_data
    if chat_data.mode == "file":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)


def run_async_stream(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


async def stream_langgraph(messages):
    output_text = ""

    async for chunk in client.runs.stream(
        None,  # threadless
        "agent",  # assistant name from langgraph.json
        input={"messages": messages},
        stream_mode="updates",
    ):
        if chunk.event != "updates":
            continue
        model_data = chunk.data.get("model")
        if not model_data:
            continue
        messages_list = model_data.get("messages", [])
        if not messages_list:
            continue
        last_msg = messages_list[-1]
        content = last_msg.get("content")
        if content:
            yield content


user_input = st.chat_input("Ask something...")


if user_input:
    st.chat_message("user").write(user_input)

    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()

    async def consume():
        async for partial in stream_langgraph(
            [{"role": "human", "content": user_input}]
        ):
            placeholder.markdown(partial)

    run_async_stream(consume())
