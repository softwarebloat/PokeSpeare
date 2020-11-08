import abc

from pydantic import BaseModel


__all__ = [
    'ShakespeareGateway',
    'ShakespeareGatewayError'
]


class ShakespeareGatewayError:
    class ShakespeareGatewayBaseError(Exception):
        pass

    class ShakespeareGatewayResponseValidationError(ShakespeareGatewayBaseError):
        pass

    class ShakespeareGatewayTooManyRequests(ShakespeareGatewayBaseError):
        pass


class ShakespeareGateway(BaseModel, abc.ABC):

    async def get_shakespeare_translation(self, text: str) -> str:
        """Translate a text from english to Shakespeare using the Shakespeare translator service

        :param text: the text in english to translate in Shakespearean way
        :type text: str
        :return: text translated in Shakespearean way
        :rtype: str
        """

        raise NotImplementedError('ShakespeareGateway.translate_to_shakespearean')
