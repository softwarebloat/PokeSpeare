import httpx
import logging

import pydantic
from pokespeare.entities.pokeapi_gateway import (
    PokeapiGateway,
    PokemonSpeciesResponse,
    PokeapiGatewayError,
)


class AsyncPokeapiGateway(PokeapiGateway):
    BASE_URL = "https://pokeapi.co/api/v2"

    async def _retrieve_pokemon_species(self, pokemon_name: str) -> PokemonSpeciesResponse:
        try:
            async with httpx.AsyncClient() as client:
                result = await client.get(f"{self.BASE_URL}/pokemon-species/{pokemon_name}/")
            result.raise_for_status()
        except httpx.HTTPError as err:
            logging.error('http error while retrieving pokemon species')
            if err.response and err.response.status_code == 404:
                logging.error('pokemon does not exists!')
                raise PokeapiGatewayError.PokeapiGatewayNotFoundError(str(err))
            else:
                raise PokeapiGatewayError.PokeapiGatewayBaseError(str(err))

        return result

    async def get_pokemon_species(self, pokemon_name: str) -> PokemonSpeciesResponse:
        res = await self._retrieve_pokemon_species(pokemon_name)
        try:
            return PokemonSpeciesResponse(**dict(res.json()))
        except pydantic.ValidationError as err:
            logging.error('Pokemon species response not valid')
            raise PokeapiGatewayError.PokeapiGatewayResponseNotValid(str(err))
