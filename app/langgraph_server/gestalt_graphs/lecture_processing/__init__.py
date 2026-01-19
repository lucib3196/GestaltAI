from dotenv import load_dotenv
from langgraph_server.gestalt_graphs.extract_derivations.graph import (
    graph as extract_derivation_graph,
    State as DerivationState,
    Derivation,
)
from langgraph_server.gestalt_graphs.extract_question.graph import (
    graph as extract_questions_graph,
    State as QuestionState,
    ExtractedQuestion,
)
from langgraph_server.gestalt_graphs.lecture_analysis.graph import (
    graph as lecture_analysis_graph,
    State as LectureAnalysisState,
    LectureAnalysis,
)
