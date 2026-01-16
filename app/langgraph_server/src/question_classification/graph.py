from pathlib import Path
from typing import List, Literal
import os
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_astradb import AstraDBVectorStore
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document

from .models import BinaryScore
from .prompts import prompt as CLASSIFICATION_PROMPT
from . import save_graph_visualization




model = init_chat_model(model="gpt-4o", model_provider="openai")
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDINGS", ""),
)

vector_store = AstraDBVectorStore(
    collection_name="topic_data",
    embedding=embeddings,
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT", None),
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN", None),
    namespace=os.getenv("ASTRA_DB_KEYSPACE", None),
)


# Define the model
class State(BaseModel):
    question: str
    topics: List[str] = []
    raw_docs: List[Document] = []
    raw_scores: List[BinaryScore] = []
    iteration: int = 0


def retrieve_examples(state: State) -> Command[Literal["grade"]]:
    retriever = vector_store.as_retriever(search_type="similarity", k=3)
    results = retriever.invoke(state.question)
    return Command(update={"raw_docs": results}, goto="grade")


def grade(state: State) -> Command[Literal[END]]:  # type: ignore
    topics = []
    raw_topics = []
    raw_scores = []
    for d in state.raw_docs:
        topic_description = d.page_content
        prompt = CLASSIFICATION_PROMPT.format(
            question=state.question, topic_description=topic_description
        )
        result = model.with_structured_output(BinaryScore).invoke(prompt)
        result = BinaryScore.model_validate(result)
        if result.score == "yes":
            raw_topics.append(d)
            topics.append(d.metadata["topic_name"])
        raw_scores.append(result)
    return Command(
        update={
            "topics": topics,
            "raw_scores": raw_scores,
        },
        goto=END,
    )


workflow = StateGraph(State)

# Define Nodes
workflow.add_node("retrieve_examples", retrieve_examples)
workflow.add_node("grade", grade)
# Connect
workflow.add_edge(START, "retrieve_examples")
workflow.add_edge("retrieve_examples", "grade")
workflow.add_edge("grade", END)


app = workflow.compile()
if __name__ == "__main__":
    input_state = State(
        question="A car is traveling along a straight rode at a constant speed of 100mph what is the total distance traveled after 5 hours"
    )
    output_path = Path(r"langgraph_server/src/question_classification/output")
    save_graph_visualization(
        app, output_path, filename="topic_classification_graph.png"
    )
    result = app.invoke(input_state)
    print("Final Result: ", result)
