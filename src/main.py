from fastapi import FastAPI

from pokespeare.routers import shakespearean_pokemon

app = FastAPI(
    title="PokeSpeare",
    description="REST API that given a Pokemon name return its Shakespearean description",
)

app.include_router(shakespearean_pokemon.router)
