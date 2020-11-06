import re
from typing import Mapping, Any

import pytest
import respx

from pokespeare.entities.pokeapi_gateway import PokeapiGatewayError
from pokespeare.adapters.pokeapi_gateway import AsyncPokeapiGateway

BASE_URL = "https://pokeapi.co/api/v2/pokemon-species/"
POKEMON_NAME = "charizard"
DEFAULT_RESPONSE = {
    'name': POKEMON_NAME,
    'flavor_text_entries': [
        {
            'flavor_text': 'a flavor description',
            'language': {'name': 'en'}
        }
    ]
}
WRONG_RESPONSE = {'name': POKEMON_NAME}


@pytest.fixture
def gateway():
    return AsyncPokeapiGateway()


@pytest.fixture
def mocked_response():
    with respx.mock() as httpx_mocker:
        yield httpx_mocker


@pytest.fixture
def mock_get_pokemon_species(mocked_response):
    def inner(status: int = None, response: Mapping[str, Any] = None):
        mocked_response.get(
            re.compile(rf'{BASE_URL}\w+'),
            status_code=status or 200,
            content=response or DEFAULT_RESPONSE
        )
    return inner


@pytest.mark.asyncio
class TestGetPokemonSpecies:

    async def test_get_pokemon_species_raise_404_on_pokemon_not_found(
        self,
        mock_get_pokemon_species,
        gateway,
    ):
        mock_get_pokemon_species(status=404)
        with pytest.raises(PokeapiGatewayError.PokeapiGatewayNotFoundError):
            await gateway.get_pokemon_species('not-a-pokemon-name')

    async def test_get_pokemon_species_raise_500_on_server_error(
        self,
        mock_get_pokemon_species,
        gateway,
    ):
        mock_get_pokemon_species(status=500)
        with pytest.raises(PokeapiGatewayError.PokeapiGatewayBaseError):
            await gateway.get_pokemon_species(POKEMON_NAME)

    async def test_wrong_response_payload(self, mock_get_pokemon_species, gateway):
        mock_get_pokemon_species(response=WRONG_RESPONSE)
        with pytest.raises(PokeapiGatewayError.PokeapiGatewayResponseNotValid):
            await gateway.get_pokemon_species(POKEMON_NAME)

    async def test_returns_response_on_success(
        self,
        mock_get_pokemon_species,
        gateway,
    ):
        mock_get_pokemon_species()
        result = await gateway.get_pokemon_species(POKEMON_NAME)
        assert result == DEFAULT_RESPONSE
