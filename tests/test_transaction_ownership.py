from decimal import Decimal

from fastapi.testclient import TestClient


def register_and_login(
    client: TestClient,
    username: str,
    email: str,
) -> dict[str, str]:
    password = f"{username}-password"
    register_response = client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_users_can_only_access_their_own_transactions(
    client: TestClient,
) -> None:
    alice_headers = register_and_login(
        client,
        username="alice",
        email="alice@example.com",
    )
    bob_headers = register_and_login(
        client,
        username="bob",
        email="bob@example.com",
    )

    create_response = client.post(
        "/api/transactions",
        headers=alice_headers,
        json={
            "amount": "15.25",
            "merchant": "Test Boba Shop",
            "category": "Dining",
            "date": "2026-09-29",
        },
    )
    assert create_response.status_code == 200
    transaction = create_response.json()
    transaction_id = transaction["id"]
    assert Decimal(transaction["amount"]) == Decimal("15.25")

    alice_list = client.get("/api/transactions", headers=alice_headers)
    assert alice_list.status_code == 200
    assert [item["id"] for item in alice_list.json()] == [transaction_id]

    bob_list = client.get("/api/transactions", headers=bob_headers)
    assert bob_list.status_code == 200
    assert bob_list.json() == []

    bob_get = client.get(
        f"/api/transactions/{transaction_id}",
        headers=bob_headers,
    )
    assert bob_get.status_code == 404

    bob_delete = client.delete(
        f"/api/transactions/{transaction_id}",
        headers=bob_headers,
    )
    assert bob_delete.status_code == 404

    alice_get = client.get(
        f"/api/transactions/{transaction_id}",
        headers=alice_headers,
    )
    assert alice_get.status_code == 200

    alice_delete = client.delete(
        f"/api/transactions/{transaction_id}",
        headers=alice_headers,
    )
    assert alice_delete.status_code == 200

    deleted_get = client.get(
        f"/api/transactions/{transaction_id}",
        headers=alice_headers,
    )
    assert deleted_get.status_code == 404
