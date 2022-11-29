import pytest
from src.sdk import Whitebox
from src.tests.v1.conftest import get_order_number, state, state_sdk
from src.tests.v1.mock_data import model_multi_create_payload
import requests_mock
from fastapi import status


@pytest.mark.order(get_order_number("sdk_init"))
def test_sdk_init(client):
    wb = Whitebox(host=client.base_url, api_key=state.api_key)
    assert wb.host == client.base_url
    assert wb.api_key == state.api_key
    state_sdk.wb = wb


@pytest.mark.order(get_order_number("sdk_create_model"))
def test_sdk_create_model(client):
    with requests_mock.Mocker() as m:
        m.post(
            url=f"{state_sdk.wb.host}/v1/models",
            json=model_multi_create_payload,
            headers={"api-key": state_sdk.wb.api_key},
        )

        model = state_sdk.wb.create_model(
            name=model_multi_create_payload["name"],
            description=model_multi_create_payload["description"],
            labels=model_multi_create_payload["labels"],
            features=model_multi_create_payload["features"],
            type=model_multi_create_payload["type"],
            probability=model_multi_create_payload["probability"],
            prediction=model_multi_create_payload["prediction"],
        )

        assert model == model_multi_create_payload


@pytest.mark.order(get_order_number("sdk_get_model"))
def test_sdk_get_model(client):
    mock_model_id = "mock_model_id"
    with requests_mock.Mocker() as m:
        m.get(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json=state.model_multi,
        )

        model = state_sdk.wb.get_model(model_id=mock_model_id)

        assert model == state.model_multi


@pytest.mark.order(get_order_number("sdk_delete_model"))
def test_sdk_delete_model(client):
    mock_model_id = "mock_model_id"

    with requests_mock.Mocker() as m:
        m.delete(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json={"status_code": status.HTTP_200_OK},
        )

        result = state_sdk.wb.delete_model(model_id=mock_model_id)
        assert result == True

    with requests_mock.Mocker() as m:
        m.delete(
            url=f"{state_sdk.wb.host}/v1/models/{mock_model_id}",
            headers={"api-key": state_sdk.wb.api_key},
            json={"status_code": status.HTTP_400_BAD_REQUEST},
        )

        result = state_sdk.wb.delete_model(model_id=mock_model_id)
        assert result == False
