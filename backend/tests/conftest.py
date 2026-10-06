from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Note, User
from app.routers import notes as notes_router


test_engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, expire_on_commit=False)
TEST_TABLES = [User.__table__, Note.__table__]


def override_get_db() -> Generator[Session, None, None]:
    with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    Base.metadata.create_all(bind=test_engine, tables=TEST_TABLES)
    app.dependency_overrides[get_db] = override_get_db

    # 接口集成测试不访问外部 Embedding 服务，也不创建 PostgreSQL ARRAY 字段。
    monkeypatch.setattr(notes_router, "rebuild_note_chunks", lambda db, note: [])

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine, tables=list(reversed(TEST_TABLES)))
