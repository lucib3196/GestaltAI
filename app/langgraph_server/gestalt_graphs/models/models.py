from pydantic import BaseModel, Field


class CodeResponse(BaseModel):
    """Output schema from the LLM for code generation."""

    code: str = Field(..., description="The generated code. Only return the code.")


class PageRange(BaseModel):
    start_page: int
    end_page: int


class Option(BaseModel):
    text: str = Field(..., description="Text of the answer choice.")
    is_correct: bool = Field(
        ..., description="True if this option is the correct answer, otherwise False."
    )
