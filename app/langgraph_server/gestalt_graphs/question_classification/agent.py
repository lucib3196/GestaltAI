from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph_server.gestalt_graphs.question_classification.graph import app, State as CState

model = init_chat_model(
    model="gpt-4o",
    model_provider="openai",
)


@tool
def classify_question(question: str):
    """Classify Question"""
    input_state = CState(question=question)
    result = app.invoke(input_state)
    topics = {"question_topics": result.get("topics")}
    return topics


tools = [classify_question]

prompt_text = (
    "You have access to a tool that retrieves context from a vector store containing classification for classifiying questions"
    "Use the tool to help answer user queries."
)

agent = create_agent(model, tools, system_prompt=prompt_text)  # Pass string directly
