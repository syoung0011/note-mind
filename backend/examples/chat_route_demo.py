from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.routers.chat import chat
from app.schemas import ChatRequest


def main() -> None:
    db = Mock()
    current_user = SimpleNamespace(id=7)
    chat_in = ChatRequest(question="我的笔记记录了什么？")
    retrieved = [object()]

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

    with (
        patch("app.routers.chat.retrieve_relevant_chunks", return_value=[]),
        patch("app.routers.chat.generate_answer") as empty_answer_mock,
    ):
        empty_response = chat(chat_in, db, current_user)

    empty_answer_mock.assert_not_called()
    assert empty_response.answer == "你的笔记中还没有可用于回答的内容。"
    print("Chat route demo passed: user scope, answer, and empty result are handled.")


if __name__ == "__main__":
    main()
