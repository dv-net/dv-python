import pytest
from dv_net_client.utils import MerchantUtilsManager


@pytest.fixture
def utils_manager():
    return MerchantUtilsManager()


def test_check_sign_valid(utils_manager):
    client_key = "my_secret_key"
    body = {"param1": "value1", "param2": 123}
    # Correct signature generated for the test
    signature = "62ee77dcd499b9bba8492cb398c8d84e07a2e4e33924b701f72410f2ca7c3315"

    assert utils_manager.check_sign(signature, client_key, body) is True


def test_check_sign_invalid(utils_manager):
    client_key = "my_secret_key"
    body = {"param1": "value1", "param2": 123}
    wrong_signature = "wrong_signature"

    assert utils_manager.check_sign(wrong_signature, client_key, body) is False


def test_generate_link(utils_manager):
    host = "https://pay.dv.net"
    store_uuid = "a1b2c3d4"
    client_id = "e5f6g7h8"
    email = "test@example.com"

    expected_link = "https://pay.dv.net/a1b2c3d4/e5f6g7h8?email=test%40example.com"
    assert utils_manager.generate_link(host, store_uuid, client_id, email) == expected_link
