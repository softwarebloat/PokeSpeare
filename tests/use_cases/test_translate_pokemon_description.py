import pytest
from pokespeare.entities.pokeapi_gateway import PokemonSpeciesResponse, FlavorText, Language

from pokespeare.use_cases import translate_pokemon_description
from pokespeare.use_cases.translate_pokemon_description import TranslatePokemonResponse

POKEMON_NAME = 'charizard'
SHAKESPEARE_TRANSLATION = 'a shakespeare translation'


@pytest.fixture
def mocked_pokeapi_response():
    return PokemonSpeciesResponse(
        name=POKEMON_NAME,
        flavor_text_entries=[
            FlavorText(
                flavor_text="a flavor description",
                language=Language(name="en")
            )
        ]
    )


@pytest.mark.asyncio
async def test_translate_pokemon_description_return_translated_description(
    mocker,
    mocked_pokeapi_response
):
    req = {
            'pokeapigateway': mocker.AsyncMock(return_value=mocked_pokeapi_response),
            'shakespearegatewaty': mocker.AsyncMock(return_value=SHAKESPEARE_TRANSLATION),
            'pokemon_name': POKEMON_NAME,
        }

    result = await translate_pokemon_description.create(req=req)

    req['pokeapigateway'].assert_called_once()
    req['shakespearegatewaty'].assert_called_once()
    assert isinstance(result, TranslatePokemonResponse)
