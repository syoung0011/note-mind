from openai import OpenAI

from app.config import settings
from app.services.retrieval import RetrievedChunk


SYSTEM_PROMPT = """你是 NoteMind 的学习笔记问答助手。
只能根据用户提供的笔记上下文回答，不要补充上下文中没有的事实。
回答应当直接、清楚，并使用中文。"""


def create_chat_client() -> OpenAI:
    if settings.dashscope_api_key is None or settings.dashscope_base_url is None:
        raise RuntimeError(
            "DASHSCOPE_API_KEY and DASHSCOPE_BASE_URL must be configured"
        )

    return OpenAI(
        api_key=settings.dashscope_api_key.get_secret_value(),
        base_url=settings.dashscope_base_url,
    )


def build_context(results: list[RetrievedChunk]) -> str:
    sections = []
    for rank, result in enumerate(results, start=1):
        sections.append(f"[片段 {rank}]\n{result.chunk.content}")
    return "\n\n".join(sections)


def generate_answer(question: str, results: list[RetrievedChunk]) -> str:
    if not question.strip():
        raise ValueError("Question must not be blank")
    if not results:
        raise ValueError("At least one retrieved chunk is required")

    context = build_context(results)
    client = create_chat_client()
    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"笔记上下文：\n{context}\n\n用户问题：\n{question}",
            },
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content
    if answer is None:
        raise RuntimeError("Chat model returned no text content")
    return answer.strip()
