from fastapi.testclient import TestClient


def register_and_login(
    client: TestClient,
    username: str,
    password: str = "notemind-test-password",
) -> dict[str, str]:
    register_response = client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_other_user_cannot_read_note(client: TestClient) -> None:
    owner_headers = register_and_login(client, "note_owner")
    other_user_headers = register_and_login(client, "other_user")

    create_response = client.post(
        "/api/notes",
        headers=owner_headers,
        json={
            "title": "Private note",
            "content": "Only the owner should be able to read this.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]
    other_response = client.get(
        f"/api/notes/{note_id}",
        headers=other_user_headers,
    )
    assert other_response.status_code == 404
