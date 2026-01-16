from src.code_generator.graphs.question_html_graph import (
    app as question_html_tool,
    State as QState,
)
from src.code_generator.models import Question
from langchain_core.documents import Document
from src.ai_tools.ai_tools import save_file

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
def generate_question_html(question: str, isAdaptive: bool):
    """
    Generate a formatted `question.html` file using established HTML conventions,
    grounded in examples retrieved from the Question HTML vectorstore.

    This tool takes a **complete, finalized natural-language question** and a flag
    indicating whether the question is **Adaptive** or **non-adaptive**.

    It returns TWO things:
    1. A fully formatted `question.html` file that follows the platform’s
       structural, semantic, and stylistic conventions.
    2. The set of retrieved reference documents used to guide the formatting
       and structure (for grounding, inspection, or debugging).

    When presenting results to the end user, you MAY display **only** the generated
    `question.html` content. The retrieved documents are provided for internal
    reference and should not be surfaced unless explicitly requested.

    Use this tool when:
    - You are converting a finalized question stub into `question.html`.
    - You need grounded examples to ensure correct HTML structure and layout.
    - You want to follow existing input, panel, and markup conventions exactly.

    The retrieved examples MUST guide the formatting of the output, but MUST NOT
    be copied verbatim. The final HTML should be original, clean, and ready for
    direct use in the educational system.
    """
    q = Question(
        question_text=question,
        solution_guide=None,
        final_answer=None,
        question_html="",
    )
    input_state: QState = {
        "question": q,
        "isAdaptive": isAdaptive,
        "question_html": None,
        "retrieved_documents": [],
        "formatted_examples": "",
    }
    result = question_html_tool.invoke(input_state)
    html = {"question_html": result.get("question_html")}
    retrieved_context: List[Document] = result.get("retrieved_documents", [])
    return html, retrieved_context


tools = [generate_question_html, save_file]

agent = create_agent(
    model,
    tools=tools,
    system_prompt=QUESTION_HTML_PROMPT,
)
