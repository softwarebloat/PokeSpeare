import pytest
import respx
from typing import Mapping, Any

from pokespeare.adapters.shakespeare_gateway import AsyncShakespeareGateway
from pokespeare.entities.shakespeare_gateway import ShakespeareGatewayError

BASE_URL = "https://api.funtranslations.com/translate/shakespeare.json"
TEXT_TO_TRANSLATE = "some random text"
DEFAULT_RESPONSE = {
  "contents": {
    "translated": "some random shakespearean translation",
    "text": "some random text",
    "translation": "shakespeare"
  }
}
WRONG_RESPONSE = {'fake': 'wrong response'}


@pytest.fixture
def gateway():
    return AsyncShakespeareGateway()


@pytest.fixture
def mocked_response():
    with respx.mock() as httpx_mocker:
        yield httpx_mocker


@pytest.fixture
def mock_get_shakespeare_translation(mocked_response):
    def inner(status: int = None, response: Mapping[str, Any] = None):
        mocked_response.post(
            BASE_URL,
            status_code=status or 200,
            content=response or DEFAULT_RESPONSE
        )
    return inner


@pytest.mark.asyncio
class TestGetShakespeareTranslation:

    async def test_get_shakespeare_translation_raise_validation_error(
        self,
        mock_get_shakespeare_translation,
        gateway,
    ):
        mock_get_shakespeare_translation(status=500)
        with pytest.raises(ShakespeareGatewayError.ShakespeareGatewayBaseError):
            await gateway.get_shakespeare_translation(TEXT_TO_TRANSLATE)

    async def test_get_shakespeare_translation_raise_key_error_on_wrong_response(
        self,
        mock_get_shakespeare_translation,
        gateway,
    ):
        mock_get_shakespeare_translation(response=WRONG_RESPONSE)
        with pytest.raises(ShakespeareGatewayError.ShakespeareGatewayResponseValidationError):
            await gateway.get_shakespeare_translation(TEXT_TO_TRANSLATE)

    async def test_return_translated_text_on_success(
        self,
        mock_get_shakespeare_translation,
        gateway,
    ):
        mock_get_shakespeare_translation()
        result = await gateway.get_shakespeare_translation(TEXT_TO_TRANSLATE)
        assert result == DEFAULT_RESPONSE['contents']['translated']
