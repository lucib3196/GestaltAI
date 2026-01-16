from src.code_generator.graphs.question_html_graph import (
    app as question_html_tool,
    State as QState,
)
from src.code_generator.models import Question
from langchain_core.documents import Document

# --- LangChain & OpenAI ---
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from typing import List

# --- Pydantic ---
from src.code_generator.prompts.prompts import QUESTION_HTML_PROMPT

model = init_chat_model(
    model="gpt-4o",
    model_provider="openai",
)


@tool
def generate_question_html(question: str, computational: bool):
    """
    Retrieve high-quality question HTML examples from the Question vectorstore.

    This tool takes a *complete natural-language question* as input and returns:
    - HTML question templates
    - Structuring patterns
    - Input components
    - Accepted formatting styles
    - Common panel layouts and markup conventions

    Use this tool when:
    - You are generating a new question.html file.
    - You need reference examples for how question files are structured.
    - You want to follow established formatting patterns, HTML structure,
      or input/parameter styles used in previous questions.

    The retrieved examples should guide the final HTML output, ensuring
    the generated question.html file is consistent, readable, and aligned
    with existing patterns in the system.
    """
    q = Question(
        question_text="A car is traveling along a straight rode at a constant speed of 100mph for 5 hours calculate the total distance traveled",
        solution_guide=None,
        final_answer=None,
        question_html="",
    )
    if computational:
        qtype = "computational"
    else:
        qtype = "static"
    input_state: QState = {
        "question": q,
        "question_type": qtype,
        "question_html": None,
        "retrieved_documents": [],
        "formatted_examples": "",
    }
    result = question_html_tool.invoke(input_state)
    html = {"question_topics": result.get("question_html")}
    retrieved_context: List[Document] = result.get("retrieved_documents", [])
    return html, retrieved_context


tools = [generate_question_html]

agent = create_agent(
    model,
    tools=tools,
    system_prompt=QUESTION_HTML_PROMPT,
)
