import json
import pytest
from pathlib import Path

from dv_net_client.dto.webhook import (
    ConfirmedWebhookResponse, UnconfirmedWebhookResponse, WithdrawalWebhookResponse
)
from dv_net_client.exceptions import DvNetInvalidWebhookException
from dv_net_client.mappers import WebhookMapper

ASSETS_DIR = Path(__file__).parent / "assets"


@pytest.fixture
def webhook_mapper():
    return WebhookMapper()


def load_asset(filename: str):
    with open(ASSETS_DIR / filename, 'r') as f:
        return json.load(f)


def test_map_confirmed_webhook(webhook_mapper):
    data = load_asset('confirmed.json')
    result = webhook_mapper.map_webhook(data)

    assert isinstance(result, ConfirmedWebhookResponse)
    assert result.type == "PaymentReceived"
    assert result.transactions.tx_id == "f35699e8-e894-454a-b32e-405b708f464c"
    assert result.wallet.id == "e24e5539-e207-4536-b529-06e2bccc187c"


def test_map_unconfirmed_webhook(webhook_mapper):
    data = load_asset('unconfirmed.json')
    result = webhook_mapper.map_webhook(data)

    assert isinstance(result, UnconfirmedWebhookResponse)
    assert result.type == "PaymentReceived"
    assert result.transactions.tx_id == "f35699e8-e894-454a-b32e-405b708f464c"
    assert result.wallet.id == "e24e5539-e207-4536-b529-06e2bccc187c"


def test_map_withdrawal_webhook(webhook_mapper):
    data = load_asset('withdrawal.json')
    result = webhook_mapper.map_webhook(data)

    assert isinstance(result, WithdrawalWebhookResponse)
    assert result.type == "WithdrawalCompleted"
    assert result.withdrawal_id == "w-f35699e8-e894-454a-b32e-405b708f464c"
    assert result.transactions.tx_hash == "tx_hash_example_withdrawal"


def test_invalid_webhook_data(webhook_mapper):
    data = load_asset('wrong.json')
    with pytest.raises(DvNetInvalidWebhookException, match="Cannot map webhook"):
        webhook_mapper.map_webhook(data)


def test_empty_webhook_data(webhook_mapper):
    data = load_asset('empty.json')
    with pytest.raises(DvNetInvalidWebhookException,
                       match='Invalid webhook format, missing "type", "withdrawal_id" or "unconfirmed_type" field'):
        webhook_mapper.map_webhook(data)
