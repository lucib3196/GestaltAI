# --- Standard Library ---
from typing import List, Optional

# --- LangChain / LangGraph ---
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.tools import tool

# --- Internal: Graph Apps & State ---
from langgraph_server.gestalt_graphs.code_generator.graphs.question_html_graph import (
    app as question_html_tool,
    State as QState,
)
from langgraph_server.gestalt_graphs.code_generator.graphs.server_js_graph import (
    app as server_js_tool,
    State as JSState,
)

# --- Internal: Models ---
from langgraph_server.gestalt_graphs.code_generator.models import Question

# --- Internal: Prompts ---
from langgraph_server.gestalt_graphs.code_generator.prompts.prompts import (
    QUESTION_HTML_PROMPT,GESTALT_AGENT
)

# --- Internal: Tools ---
from langgraph_server.gestalt_graphs.ai_tools.ai_tools import (
    prepare_zip,
    save_file,
)


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


@tool
def generate_server_js(
    question_html: str,
    solution_guide: Optional[str] = None,
):
    """
    Generate a fully structured `server.js` file that implements the backend
    logic for an **adaptive question**, grounded in retrieved reference examples.

    This tool takes a **complete `question.html` file** and an optional
    **solution guide**, and synthesizes the JavaScript code required to:
    - Generate dynamic parameters at runtime
    - Compute correct answers programmatically
    - Expose values and results to the frontend question interface

    It returns TWO things:
    1. A generated `server.js` file containing the backend computation and
       parameter-generation logic for the question.
    2. The set of retrieved reference documents used to guide the structure,
       patterns, and conventions of the generated JavaScript.

    The retrieved documents serve as **grounding context** and are intended for
    internal inspection, debugging, or traceability. They SHOULD NOT be exposed
    to end users unless explicitly requested.

    Use this tool when:
    - You are generating backend logic for an **adaptive** question.
    - The `question.html` file contains dynamic variables or placeholders.
    - You need to follow established server-side conventions for parameter
      generation, computation, and data exposure.

    The retrieved examples MUST inform the structure and patterns of the output,
    but MUST NOT be copied verbatim. The generated JavaScript should be original,
    readable, and ready for direct use within the platform’s execution environment.
    """
    question = Question(
        question_text="",
        solution_guide=solution_guide,
        final_answer=None,
        question_html=question_html,
    )
    input_state: JSState = {
        "question": question,
        "isAdaptive": True,
        "server_js": None,
        "retrieved_documents": [],
        "formatted_examples": "",
    }
    result = server_js_tool.invoke(input_state)
    server = {"server_jd": result.get("server_js")}
    retrieved_context: List[Document] = result.get("retrieved_documents", [])
    return server, retrieved_context


tools = [generate_question_html, prepare_zip, generate_server_js]

agent = create_agent(
    model,
    tools=tools,
    system_prompt=GESTALT_AGENT,
)
