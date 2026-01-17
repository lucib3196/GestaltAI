from pydantic import BaseModel
from typing import Dict, Literal, List

ALLOWED_MODE = Literal["text", "file"]

CHAT_NAMES = Literal[
    "gestalt_module_builder",
    "module_builder_image",
    "question_classifier",
    "gestalt_build_agent",
    "course_classifier",
]


class ChatOption(BaseModel):
    label: str
    url: str
    description: str
    mode: ALLOWED_MODE = "text"
    active: bool = False


CHAT_OPTIONS: Dict[CHAT_NAMES, ChatOption] = {
    "gestalt_module_builder": ChatOption(
        label="Gestalt Module Builder",
        url="agent_gestalt_module",
        description=(
            "Generate a complete, ready-to-use Gestalt module in one pass. "
            "This tool creates and packages all required files "
            "(question.html, solution.html, server logic, and metadata) "
            "from finalized text input, with minimal iteration."
        ),
        active=True,
    ),
    "gestalt_build_agent": ChatOption(
        label="Gestalt Build Agent",
        url="agent_gestalt",
        description=(
            "Incrementally generate and refine individual or grouped files "
            "(question.html, solution.html, server logic, metadata) using "
            "Gestalt’s modular, tool-based workflow. Designed for "
            "fine-grained control, iteration, and targeted file generation."
        ),
        active=True,
    ),
    "module_builder_image": ChatOption(
        label="Module Builder (Image)",
        url="/moc/module-builder",
        description="Generate a complete multi-file module from image input.",
        mode="file",
    ),
    "question_classifier": ChatOption(
        label="Question Classifier",
        url="question_classification",
        description="Classify question type and intent.",
        active=True,
    ),
    "course_classifier": ChatOption(
        label="Course Classifier",
        url="/moc/classification",
        description="Map questions to courses or curricula.",
    ),
}
