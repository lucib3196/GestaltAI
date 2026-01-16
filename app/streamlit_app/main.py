import asyncio
import streamlit as st
from settings import get_settings
from chat_modes import (
    OPTIONS,
    CHAT_OPTIONS,
    ChatOption,
)
from client import stream_langgraph, client

settings = get_settings()


def get_loop():
    if "event_loop" not in st.session_state:
        loop = asyncio.new_event_loop()
        st.session_state.event_loop = loop
    else:
        loop = st.session_state.event_loop
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            st.session_state.event_loop = loop

    asyncio.set_event_loop(loop)
    return loop


async def get_thread_id():
    return await client.threads.create()


def run_async_stream(coro):
    loop = get_loop()
    return loop.run_until_complete(coro)


# Basic Set up
if "thread_id" not in st.session_state:
    thread = run_async_stream(get_thread_id())
    st.session_state.thread_id = thread["thread_id"]

if "messages" not in st.session_state:
    st.session_state.messages = []


if settings.environment == "local":
    # st.session_state.thread_id
    title = f"Gestalt AI (Local)"
    if st.session_state.thread_id:
        title += str(st.session_state.thread_id)
else:
    title = "Gestalt AI"


st.set_page_config(page_title=title, layout="centered")
st.title(title)


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


user_input = st.chat_input("Ask something...")


for message in st.session_state.messages:
    role = message.get("role", "ai")
    with st.chat_message(role):
        st.markdown(message["content"])

if user_input:
    st.chat_message("user").markdown(user_input)
    user_message = {"role": "user", "content": user_input}
    st.session_state.messages.append(user_message)
    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()
    tool_placeholder = assistant_box.container()

    async def consume():
        buffer = ""
        tool_calls_rendered = set()
        async for token in stream_langgraph(
            [{"role": "human", "content": user_input}],
            st.session_state.thread_id,
            st.session_state.chat_data.url,
        ):
            content = token.get("content")
            if content:
                buffer += content
                placeholder.markdown(buffer)
            tool_calls = token.get("tool_calls")
            if tool_calls:
                for call in tool_calls:
                    call_id = call.get("id")
                    if call_id in tool_calls_rendered:
                        continue
                    tool_calls_rendered.add(call_id)
                    with tool_placeholder:
                        with st.expander(f"Tool call: `{call['name']}`", expanded=True):
                            st.json(call["args"])
            st.session_state.messages.append({"role": "assistant", "content": buffer})

    run_async_stream(consume())
