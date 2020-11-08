import pytest
from fastapi.testclient import TestClient

from main import app
from pokespeare.use_cases.translate_pokemon_description import TranslatePokemonResponse

client = TestClient(app)


@pytest.mark.integration
def test_shakesperean_pokemon_endpoint_success():
    response = client.get("/pokemon/charizard")
    assert response.status_code == 200
    assert isinstance(response.content(), TranslatePokemonResponse)


@pytest.mark.integration
def test_shakesperean_pokemon_endpoint_raise_exception_if_called_more_than_five_times():
    for _ in range(5):
        client.get("/pokemon/charizard")

    response = client.get("/pokemon/charizard")
    assert response.status_code == 429


@pytest.mark.integration
def test_shakesperean_pokemon_endpoint_pokemon_not_found():
    response = client.get("/pokemon/goku")

    assert response.status_code == 404
