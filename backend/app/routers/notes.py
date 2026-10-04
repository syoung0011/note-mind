from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Note, User
from app.routers.auth import get_current_user
from app.schemas import NoteCreate, NotePublic, NoteUpdate

router = APIRouter(
    prefix="/api/notes",
    tags=["notes"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)


@router.post("", response_model=NotePublic, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Note:
    note = Note(
        user_id=current_user.id,
        title=note_in.title,
        content=note_in.content,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=list[NotePublic])
def list_notes(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Note]:
    notes = db.scalars(
        select(Note)
        .where(Note.user_id == current_user.id)
        .order_by(Note.created_at.desc(), Note.id.desc())
    ).all()
    return list(notes)


@router.get(
    "/{note_id}",
    response_model=NotePublic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Note not found",
        },
    },
)
def get_note(
    note_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Note:
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@router.put(
    "/{note_id}",
    response_model=NotePublic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Note not found",
        },
    },
)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Note:
    note = db.scalar(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.title = note_in.title
    note.content = note_in.content
    db.commit()
    db.refresh(note)
    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Note deleted successfully",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Note not found",
        },
    },
)
def delete_note(
    note_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()
