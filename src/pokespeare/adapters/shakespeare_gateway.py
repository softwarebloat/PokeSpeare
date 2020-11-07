import logging

import httpx
from pokespeare.entities.shakespeare_gateway import ShakespeareGateway, ShakespeareGatewayError


class AsyncShakespeareGateway(ShakespeareGateway):
    BASE_URL = "https://api.funtranslations.com/translate/shakespeare.json"

    async def _translate_to_shakespearean(self, text: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                result = await client.post(
                    self.BASE_URL,
                    data={'text': text},
                )
            result.raise_for_status()
        except httpx.HTTPError as err:
            logging.error(
                'http error while retrieving Shakespeare translation',
                {'error': str(err)}
            )
            raise ShakespeareGatewayError.ShakespeareGatewayBaseError(str(err))

        return result

    async def get_shakespeare_translation(self, text: str) -> str:
        res = await self._translate_to_shakespearean(text)
        try:
            return res.json()['contents']['translated']
        except KeyError as err:
            logging.error('Shakespeare translator response not valid', {'error': str(err)})
            raise ShakespeareGatewayError.ShakespeareGatewayResponseValidationError(str(err))
