from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

    model_config = ConfigDict(str_strip_whitespace=True)


class ChatCitation(BaseModel):
    note_id: int
    note_title: str
    chunk_index: int = Field(ge=0)
    content: str
    score: float = Field(ge=-1.0, le=1.0)


class ChatResponse(BaseModel):
    answer: str
    citations: list[ChatCitation]
