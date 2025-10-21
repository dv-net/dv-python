import pytest
from unittest.mock import MagicMock

from dv_net_client.client import MerchantClient
from dv_net_client.dto import merchant_client as mc_dto
from dv_net_client.exceptions import (
    DvNetUndefinedHostException, DvNetUndefinedXApiKeyException
)


@pytest.fixture
def mock_http_client():
    return MagicMock()


@pytest.fixture
def client(mock_http_client):
    return MerchantClient(
        http_client=mock_http_client,
        host="https://fake.host",
        x_api_key="fake-api-key"
    )


def test_get_exchange_balances(client, mock_http_client):
    mock_response = {
        "data": {
            "total_usd": "1000.00",
            "balances": [
                {"amount": "1.0", "amount_usd": "500.00", "currency": "BTC"}
            ]
        }
    }
    mock_http_client.send_request.return_value = (200, mock_response)

    result = client.get_exchange_balances()

    assert isinstance(result, mc_dto.TotalExchangeBalanceResponse)
    assert result.total_usd == "1000.00"
    mock_http_client.send_request.assert_called_once()


def test_client_initialization_exceptions():
    with pytest.raises(DvNetUndefinedHostException):
        client = MerchantClient(x_api_key="key")
        client.get_exchange_balances()

    with pytest.raises(DvNetUndefinedXApiKeyException):
        client = MerchantClient(host="host")
        client.get_exchange_balances()
