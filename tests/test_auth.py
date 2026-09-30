from fastapi.testclient import TestClient


def test_login_requires_only_email_and_password(client: TestClient) -> None:
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "alice-password",
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "alice-password",
        },
    )

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert login_response.json()["access_token"]


def test_protected_route_rejects_missing_token(client: TestClient) -> None:
    response = client.get("/api/transactions")

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
