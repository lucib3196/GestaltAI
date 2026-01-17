from typing import List, Literal
from pydantic import BaseModel


class TopicDescription(BaseModel):
    name: str
    description: str
    discipline: List[str]


class FullTopicDescriptionList(BaseModel):
    topics: List[TopicDescription]


class BinaryScore(BaseModel):
    score: Literal["yes", "no"]
    reasoning: str
