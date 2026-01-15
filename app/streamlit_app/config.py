from pydantic import BaseModel
from typing import Dict, Literal, List

CHAT_NAMES = Literal[
    "module_builder_text",
    "module_builder_image",
    "question_classifier",
    "file_generator",
    "course_classifier",
]
OPTIONS: List[CHAT_NAMES] = [
    "module_builder_text",
    "module_builder_image",
    "question_classifier",
    "file_generator",
    "course_classifier",
]


class ChatOption(BaseModel):
    label: str
    url: str
    description: str


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
    ),
    "file_generator": ChatOption(
        label="Single File Generator",
        url="/moc/file-generator",
        description="Generate a specific file with focused functionality.",
    ),
    "question_classifier": ChatOption(
        label="Question Classifier",
        url="/moc/classification",
        description="Classify question type and intent.",
    ),
    "course_classifier": ChatOption(
        label="Course Classifier",
        url="/moc/classification",
        description="Map questions to courses or curricula.",
    ),
}
