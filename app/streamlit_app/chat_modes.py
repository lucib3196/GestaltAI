from pydantic import BaseModel
from typing import Dict, Literal, List

ALLOWED_MODE = Literal["text", "file"]

CHAT_NAMES = Literal[
    "module_builder_text",
    "module_builder_image",
    "question_classifier",
    "file_generator",
    "course_classifier",
]
OPTIONS: List[CHAT_NAMES] = [
    # "module_builder_text",
    # "module_builder_image",
    "question_classifier",
    "file_generator",
    # "course_classifier",
]


class ChatOption(BaseModel):
    label: str
    url: str
    description: str
    mode: ALLOWED_MODE = "text"
    active: bool = False


CHAT_OPTIONS: Dict[CHAT_NAMES, ChatOption] = {
    "module_builder_text": ChatOption(
        label="Module Builder (Text)",
        url="/moc/module-builder",
        description="Generate a complete multi-file module from text input.",
    ),
    "module_builder_image": ChatOption(
        label="Module Builder (Image)",
        url="/moc/module-builder",
        description="Generate a complete multi-file module from image input.",
        mode="file",
    ),
    "file_generator": ChatOption(
        label="Single File Generator",
        url="agent_gestalt",
        description="Generate a specific file with focused functionality.",
        active=True,
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
