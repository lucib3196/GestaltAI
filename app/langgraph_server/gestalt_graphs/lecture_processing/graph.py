from . import *
from pydantic import BaseModel

# --- Standard Library ---
import asyncio
from pathlib import Path

# --- Third-Party ---
from pydantic import BaseModel
from langsmith import Client
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import List

# --- Local Application ---
from langgraph_server.gestalt_graphs.models import LectureAnalysis
from langgraph_server.parsers import PDFMultiModalLLM
from langgraph_server.gestalt_graphs.utils import (
    save_graph_visualization,
    to_serializable,
    extract_langsmith_prompt,
)


class State(BaseModel):
    lecture_pdf: str | Path
    lecture_analysis: LectureAnalysis | None = None
    extracted_questions: List[ExtractedQuestion] = []
    derivations: List[Derivation] = []


async def analysis(state: State):
    result = await lecture_analysis_graph.ainvoke(
        LectureAnalysisState(lecture_pdf=state.lecture_pdf)
    )
    result = LectureAnalysisState.model_validate(result)
    return {"lecture_analysis": result.analysis}


async def extract_derivations(state: State):
    result = await extract_derivation_graph.ainvoke(
        DerivationState(lecture_pdf=state.lecture_pdf)
    )
    result = DerivationState.model_validate(result)
    return {"derivations": result.derivations}


async def extract_questions(state: State):
    result = await extract_questions_graph.ainvoke(
        QuestionState(lecture_pdf=state.lecture_pdf)
    )
    result = QuestionState.model_validate(result)
    return {"questions": result.questions}


builder = StateGraph(State)

# Add nodes
builder.add_node("analysis", analysis)
builder.add_node("extract_derivations", extract_derivations)
builder.add_node("extract_questions", extract_questions)

# Fan-out from START
builder.add_edge(START, "analysis")
builder.add_edge(START, "extract_derivations")
builder.add_edge(START, "extract_questions")

# All nodes terminate at END
builder.add_edge("analysis", END)
builder.add_edge("extract_derivations", END)
builder.add_edge("extract_questions", END)

graph = builder.compile()


if __name__ == "__main__":
    # Path to the lecture PDF
    pdf_path = Path(r"langgraph_server/data/Lecture_02_03.pdf").resolve()

    output_path = Path(
        r"langgraph_server/gestalt_graphs/lecture_processing/output"
    ).resolve()

    save_path = output_path
    save_graph_visualization(graph, save_path, "graph.png")

    # Create graph input state
    graph_input = State(lecture_pdf=pdf_path)

    # Run the async graph and print the response
    try:
        response = asyncio.run(graph.ainvoke(graph_input))
        print("\n--- Graph Response ---")
        print(response)
        import json

        data_path = save_path / "output.json"
        data_path.write_text(json.dumps(to_serializable(response)))
    except Exception as e:
        print("\n❌ Error while running graph:")
        print(e)
