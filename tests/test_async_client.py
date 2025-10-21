import pytest
from unittest.mock import AsyncMock

from dv_net_client.async_client import AsyncMerchantClient
from dv_net_client.dto import merchant_client as mc_dto
from dv_net_client.exceptions import (
    DvNetUndefinedHostException, DvNetUndefinedXApiKeyException
)


@pytest.fixture
def mock_async_http_client():
    return AsyncMock()


@pytest.fixture
def async_client(mock_async_http_client):
    return AsyncMerchantClient(
        http_client=mock_async_http_client,
        host="https://fake.host",
        x_api_key="fake-api-key"
    )


@pytest.mark.asyncio
async def test_get_exchange_balances_async(async_client, mock_async_http_client):
    mock_response = {
        "data": {
            "total_usd": "1000.00",
            "balances": [
                {"amount": "1.0", "amount_usd": "500.00", "currency": "BTC"}
            ]
        }
    }
    mock_async_http_client.send_request.return_value = (200, mock_response)

    result = await async_client.get_exchange_balances()

    assert isinstance(result, mc_dto.TotalExchangeBalanceResponse)
    assert result.total_usd == "1000.00"
    mock_async_http_client.send_request.assert_called_once()


@pytest.mark.asyncio
async def test_async_client_initialization_exceptions():
    with pytest.raises(DvNetUndefinedHostException):
        client = AsyncMerchantClient(x_api_key="key")
        await client.get_exchange_balances()

    with pytest.raises(DvNetUndefinedXApiKeyException):
        client = AsyncMerchantClient(host="host")
        await client.get_exchange_balances()
