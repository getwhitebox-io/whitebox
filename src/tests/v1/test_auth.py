import pytest
from src.tests.v1.conftest import get_order_number
from src.tests.v1.mock_data import login_payload, register_payload
from fastapi import status

access_token = ""


@pytest.mark.order(get_order_number("auth_unauthorized_me"))
def test_me(client):
    response = client.post("/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# @pytest.mark.order(test_order_map["auth"]["login"])
# def test_login(client):
#     response = client.post("/v1/auth/token", data=login_payload)
#     global access_token
#     access_token = " ".join(
#         (response.json()["token_type"].capitalize(), response.json()["access_token"])
#     )
#     assert response.json()["access_token"] is not None
#     assert len(response.json()["access_token"]) == 311


# @pytest.mark.order(test_order_map["auth"]["authorized_me"])
# def test_me(client):
#     global access_token
#     response = client.post("/v1/auth/me", headers={"Authorization": access_token})
#     assert response.json()["email"] == register_payload["email"]
#     assert response.json()["password"] is None
