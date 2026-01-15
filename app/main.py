import streamlit as st
import os
from langgraph_sdk import get_client
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = get_client(url = "https://cloudtest2-372e7c35e8c95922a80b43de91a4b917.us.langgraph.app", api_key=os.getenv("LANGSMITH_API_KEY"))

st.set_page_config(page_title="LangGraph Streaming", layout="centered")
st.title("🧠 LangGraph Streaming Chat")

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
        stream_mode="updates"
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