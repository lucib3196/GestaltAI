from pydantic import BaseModel, Field
from typing import List
from .question import QuestionTypes
from .models import PageRange, Option

# --- Standard Library ---
from typing import Optional, List


class ExtractedQuestion(BaseModel):
    """
    A general-purpose representation of a question and its solution extracted
    from lecture notes, handwritten work, PDFs, slides, or any multimodal source.
    This model does not assume a specific question format; instead, it captures
    the essential components that may appear across conceptual, computational,
    derivation-based, or multiple-choice problems.
    """

    question_text: str = Field(
        ..., description="The raw question extracted from the source material."
    )

    qtype: QuestionTypes = Field(
        ...,
        description=(
            "The detected type of the question (e.g., 'conceptual', 'computational', "
            "'derivation', 'multiple_choice', 'short_answer')."
        ),
    )

    topics: List[str] = Field(
        default_factory=list,
        description=(
            "A list of detected topics, keywords, or concepts associated with the question."
        ),
    )

    options: List["Option"] | None = Field(
        default=None,
        description=(
            "If the question is multiple-choice, the extracted answer options. "
            "Otherwise, this field is None."
        ),
    )

    reference: PageRange | None = Field(
        default=None,
        description=(
            "Where in the lecture material the question was found. Can be a page range, "
            "slide number, or location index. Optional."
        ),
    )

    solution: str | None = Field(
        default=None,
        description="The extracted or reconstructed solution guide corresponding to the question.",
    )

    def as_string(self) -> str:
        """Return a formatted string representation of the extracted question."""
        base = [
            "### **Extracted Question**",
            f"**Type:** {self.qtype}",
            f"**Question:** {self.question_text}",
            f"**Topics:** {', '.join(self.topics) if self.topics else 'N/A'}",
        ]

        # Options
        if self.options:
            options_formatted = "\n".join(
                [
                    f"- {'✅ ' if opt.is_correct else ''}{opt.text}"
                    for opt in self.options
                ]
            )
            base.append(f"**Options:**\n{options_formatted}")

        # Solution
        base.append(f"**Solution:**\n{self.solution or 'N/A'}")

        # Explanation
        # Reference
        base.append(f"**Reference:** {self.reference or 'N/A'}")

        return "\n\n".join(base) + "\n"


class ConceptualQuestion(BaseModel):
    question: str = Field(..., description="The conceptual question being asked.")
    topics: List[str] = Field(
        ...,
        description="A list of three key topics or concepts that this question addresses.",
    )
    options: List["Option"] = Field(
        ...,
        description="Multiple-choice options corresponding to possible answers for the question.",
    )
    reference: "PageRange" = Field(
        ...,
        description="Page range within the lecture material where the concept or question originates.",
    )
    explanation: str = Field(
        ...,
        description="A concise explanation of the correct answer intended to help students understand the reasoning.",
    )

    def as_string(self) -> str:
        """Return a formatted string representation of the conceptual question."""
        options_formatted = "\n".join(
            [f"- {'✅ ' if opt.is_correct else ''}{opt.text}" for opt in self.options]
        )
        topics_formatted = ", ".join(self.topics)

        return (
            f"### **Conceptual Question**\n"
            f"**Question:** {self.question}\n\n"
            f"**Topics:** {topics_formatted}\n\n"
            f"**Options:**\n{options_formatted}\n\n"
            f"**Explanation:** {self.explanation}\n\n"
            f"**Reference:** {self.reference}\n"
        )


class Derivation(BaseModel):
    derivation_title: str = Field(
        ...,
        description="A short, concise title describing what the derivation focuses on.",
    )
    derivation_stub: str = Field(
        ...,
        description="A brief statement of the equation, relationship, or expression being derived.",
    )
    steps: List[str] = Field(
        ...,
        description="An ordered list of logical or mathematical steps used to carry out the derivation.",
    )
    reference: PageRange = Field(
        ...,
        description="The range of pages within the lecture material where this derivation appears.",
    )

    def as_string(self) -> str:
        steps_formatted = "\n".join(
            [f"{i+1}. {step}" for i, step in enumerate(self.steps)]
        )
        return (
            f"### **{self.derivation_title}**\n"
            f"**Stub:** {self.derivation_stub}\n\n"
            f"**Steps:**\n{steps_formatted}\n\n"
            f"**Reference:** {self.reference}\n"
        )


class LectureAnalysis(BaseModel):
    lecture_title: str = Field(
        ...,
        description="A concise, descriptive title summarizing the main focus of the lecture.",
    )

    lecture_summary: str = Field(
        ...,
        description=(
            "A concise, high-level summary of the lecture, written in clear "
            "pedagogical language. Should capture the main ideas, not details."
        ),
    )

    core_topics: List[str] = Field(
        ...,
        description=(
            "A list of the primary concepts or topics covered in the lecture. "
            "Each item should be a short noun phrase (e.g., 'Bernoulli equation')."
        ),
    )

    learning_objectives: List[str] = Field(
        ...,
        description=(
            "What a student should understand or be able to do after the lecture. "
            "Each objective should start with an action verb (e.g., 'derive', 'explain')."
        ),
    )

    assumed_prerequisites: Optional[List[str]] = Field(
        default=None,
        description=(
            "Concepts or courses the lecture assumes prior knowledge of "
            "(e.g., 'basic calculus', 'Newtonian mechanics')."
        ),
    )

    lecture_type: Optional[str] = Field(
        default=None,
        description=(
            "The primary nature of the lecture, such as 'conceptual', "
            "'derivation-heavy', 'computational', or 'mixed'."
        ),
    )
