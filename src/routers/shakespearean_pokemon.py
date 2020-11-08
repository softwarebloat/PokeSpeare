from fastapi import APIRouter, Path, HTTPException
from pokespeare.adapters.pokeapi_gateway import AsyncPokeapiGateway
from pokespeare.adapters.shakespeare_gateway import AsyncShakespeareGateway
from pokespeare.entities.shakespeare_gateway import ShakespeareGatewayError

from pokespeare.use_cases import translate_pokemon_description
from pokespeare.use_cases.translate_pokemon_description import TranslatePokemonResponse

router = APIRouter()


@router.get("/pokemon/{pokemon_name}", response_model=TranslatePokemonResponse)
async def shakespearean_pokemon(
    pokemon_name: str = Path(..., description='The pokemon to retrieve the Shakespearean translation')  # noqa: E501
):
    """
    Retrieve the shakespearean translation of the chosen pokemon description.\n
    This api will call the pokeapi service to retrieve information about the specified pokemon.
    Then it'll call the shakespeare translator service to translate the description retrieved and
    returns it
    """

    try:
        return await translate_pokemon_description.create(req={
            'pokeapigateway': AsyncPokeapiGateway().get_pokemon_species,
            'shakespearegatewaty': AsyncShakespeareGateway().get_shakespeare_translation,
            'pokemon_name': pokemon_name,
        })
    except ShakespeareGatewayError.ShakespeareGatewayTooManyRequests as err:
        raise HTTPException(status_code=429, detail=str(err))
