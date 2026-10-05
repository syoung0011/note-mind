from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models import Note, NoteChunk
from app.services.chunking import split_text
from app.services.embeddings import generate_embeddings


def rebuild_note_chunks(db: Session, note: Note) -> list[NoteChunk]:
    texts = split_text(note.content)
    embeddings = generate_embeddings(texts)

    if len(texts) != len(embeddings):
        raise RuntimeError("Embedding count does not match chunk count")

    db.execute(delete(NoteChunk).where(NoteChunk.note_id == note.id))

    note_chunks = [
        NoteChunk(
            note_id=note.id,
            user_id=note.user_id,
            chunk_index=chunk_index,
            content=text,
            embedding=embedding,
        )
        for chunk_index, (text, embedding) in enumerate(zip(texts, embeddings))
    ]
    db.add_all(note_chunks)
    return note_chunks
