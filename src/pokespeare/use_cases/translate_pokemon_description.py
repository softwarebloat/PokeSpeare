from typing import TypedDict, Callable, Awaitable

from pokespeare.entities.pokeapi_gateway import PokemonSpeciesResponse
from pydantic import BaseModel

TranslatePokemonDescriptionRequest = TypedDict('TranslatePokemonDescriptionRequest', {
    'pokeapigateway': Callable[[str], Awaitable[PokemonSpeciesResponse]],
    'shakespearegatewaty': Callable[[str], Awaitable[str]],
    'pokemon_name': str,
})


class TranslatePokemonResponse(BaseModel):
    name: str
    description: str


async def create(req: TranslatePokemonDescriptionRequest) -> TranslatePokemonResponse:
    """
    Business logic that use the injected gateways to call the pokeapi and Shakespeare translation
    services and build the response with the Shakesperean translated pokemon description.
    """

    pokeapi = req['pokeapigateway']
    shakespeare = req['shakespearegatewaty']

    pokemon = await pokeapi(req['pokemon_name'])
    original_description = next(
        x.flavor_text for x in pokemon.flavor_text_entries if x.language.name == 'en'
    )
    translated_description = await shakespeare(original_description)

    return TranslatePokemonResponse(name=pokemon.name, description=translated_description)
