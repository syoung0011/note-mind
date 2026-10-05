from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.models import NoteChunk
from app.routers.chat import INSUFFICIENT_CONTEXT_ANSWER, chat
from app.schemas import ChatRequest
from app.services.retrieval import RetrievedChunk


def main() -> None:
    db = Mock()
    current_user = SimpleNamespace(id=7)
    chat_in = ChatRequest(question="我的笔记记录了什么？")
    chunk = NoteChunk(
        id=11,
        note_id=5,
        user_id=7,
        chunk_index=2,
        content="笔记中的事实",
        embedding=[1.0, 0.0],
    )
    retrieved = [
        RetrievedChunk(chunk=chunk, note_title="测试笔记", score=0.91)
    ]

    with (
        patch(
            "app.routers.chat.retrieve_relevant_chunks",
            return_value=retrieved,
        ) as retrieve_mock,
        patch(
            "app.routers.chat.generate_answer",
            return_value="笔记中的回答",
        ) as answer_mock,
    ):
        response = chat(chat_in, db, current_user)

    retrieve_mock.assert_called_once_with(db, 7, chat_in.question)
    answer_mock.assert_called_once_with(chat_in.question, retrieved)
    assert response.answer == "笔记中的回答"
    assert len(response.citations) == 1
    assert response.citations[0].note_id == 5
    assert response.citations[0].note_title == "测试笔记"
    assert response.citations[0].chunk_index == 2
    assert response.citations[0].content == "笔记中的事实"
    assert response.citations[0].score == 0.91

    with (
        patch("app.routers.chat.retrieve_relevant_chunks", return_value=[]),
        patch("app.routers.chat.generate_answer") as empty_answer_mock,
    ):
        empty_response = chat(chat_in, db, current_user)

    empty_answer_mock.assert_not_called()
    assert empty_response.answer == INSUFFICIENT_CONTEXT_ANSWER
    assert empty_response.citations == []
    print("Chat route demo passed: user scope, answer, and empty result are handled.")


if __name__ == "__main__":
    main()
