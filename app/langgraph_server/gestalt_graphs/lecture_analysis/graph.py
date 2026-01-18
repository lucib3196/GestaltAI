from langgraph_server.gestalt_graphs.models import SectionBreakdown
from pydantic import BaseModel, Field
import asyncio
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field
from langsmith import Client
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

from langgraph_server.gestalt_graphs.utils import extract_langsmith_prompt
from langgraph_server.gestalt_graphs.models import Derivation
from langgraph_server.parsers import PDFMultiModalLLM


llm = init_chat_model(model="gpt-5-mini", model_provider="openai")



class LectureAnalysis(BaseModel):
    lecture_title: str = Field(
        ..., description="A consise title of what the lecture covers"
    )
    lecture_summary: str = Field(
        ...,
        description="A consise and to the point description of what the lecture covers",
    )
    derivations: SectionBreakdown = Field(
        ..., description="Wheter the content material contains derivations"
    )
    computational_problems: SectionBreakdown = Field(
        ...,
        description="Wether the lecture content contains any computational questions",
    )
