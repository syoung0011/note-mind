from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user
from app.schemas import ChatRequest, ChatResponse
from app.services.answering import generate_answer
from app.services.retrieval import retrieve_relevant_chunks

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
        return ChatResponse(answer="你的笔记中还没有可用于回答的内容。")
    answer = generate_answer(chat_in.question, results)
    return ChatResponse(answer=answer)
