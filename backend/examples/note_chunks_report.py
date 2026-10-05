from collections import defaultdict

from sqlalchemy import select

from app.database import SessionLocal
from app.models import NoteChunk


def main() -> None:
    with SessionLocal() as db:
        chunks = db.scalars(
            select(NoteChunk).order_by(NoteChunk.note_id, NoteChunk.chunk_index)
        ).all()

    chunks_by_note: dict[int, list[NoteChunk]] = defaultdict(list)
    for chunk in chunks:
        chunks_by_note[chunk.note_id].append(chunk)

    if not chunks_by_note:
        print("No note chunks found.")
        return

    for note_id, note_chunks in chunks_by_note.items():
        indexes = [chunk.chunk_index for chunk in note_chunks]
        dimensions = sorted({len(chunk.embedding) for chunk in note_chunks})
        print(
            f"note_id={note_id} chunks={len(note_chunks)} "
            f"indexes={indexes} dimensions={dimensions}"
        )


if __name__ == "__main__":
    main()
