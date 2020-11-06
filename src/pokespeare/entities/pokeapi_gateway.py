import abc

from pydantic import BaseModel
from typing import List


__all__ = [
    'PokeapiGateway',
    'PokemonSpeciesResponse',
    'PokeapiGatewayError',
]


class Language(BaseModel):
    name: str


class FlavorText(BaseModel):
    flavor_text: str
    language: Language


class PokemonSpeciesResponse(BaseModel):
    name: str
    flavor_text_entries: List[FlavorText]


class PokeapiGatewayError:
    class PokeapiGatewayBaseError(Exception):
        pass

    class PokeapiGatewayNotFoundError(PokeapiGatewayBaseError):
        pass

    class PokeapiGatewayResponseNotValid(PokeapiGatewayBaseError):
        pass


class PokeapiGateway(BaseModel, abc.ABC):

    async def get_pokemon_species(self, pokemon_name: str) -> PokemonSpeciesResponse:
        """Retrieve the pokemon specie by pokemon name from the pokeapi service and return the name
        and descriptions of it

        :param pokemon_name: the name of the pokemon to retrieve
        :type pokemon_name: str
        :return: name and description of the chosen pokemon
        :rtype: PokemonSpeciesResponse
        """
        raise NotImplementedError('PokeapiGateway.get_pokemon_species')
