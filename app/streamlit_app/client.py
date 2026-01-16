import asyncio
import streamlit as st
from langgraph_sdk import get_client
from settings import get_settings
from chat_modes import (
    OPTIONS,
    CHAT_OPTIONS,
    ChatOption,
)


settings = get_settings()

client = get_client(
    url=settings.langgraph_local_url,
    api_key=settings.langsmith_api_key,
)





async def stream_langgraph(messages, thread_id: str | None, assistant_id: str):
    async for chunk in client.runs.stream(
        thread_id,
        assistant_id=assistant_id,
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
        print("Last message in stream", last_msg)
        if last_msg:
            yield last_msg

