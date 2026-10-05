from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user
from app.schemas import ChatCitation, ChatRequest, ChatResponse
from app.services.answering import generate_answer
from app.services.retrieval import RetrievedChunk, retrieve_relevant_chunks

INSUFFICIENT_CONTEXT_ANSWER = "我在你的笔记中没有找到足够相关的内容来回答这个问题。"


def build_citations(results: list[RetrievedChunk]) -> list[ChatCitation]:
    citations: list[ChatCitation] = []
    for result in results:
        citations.append(
            ChatCitation(
                note_id=result.chunk.note_id,
                note_title=result.note_title,
                chunk_index=result.chunk.chunk_index,
                content=result.chunk.content,
                score=result.score,
            )
        )
    return citations


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)


@router.post("", response_model=ChatResponse)
def chat(
    chat_in: ChatRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ChatResponse:
    results = retrieve_relevant_chunks(db, current_user.id, chat_in.question)
    if not results:
        return ChatResponse(answer=INSUFFICIENT_CONTEXT_ANSWER, citations=[])
    answer = generate_answer(chat_in.question, results)
    return ChatResponse(answer=answer, citations=build_citations(results))
