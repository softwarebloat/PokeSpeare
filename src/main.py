from fastapi import FastAPI

from routers import shakespearean_pokemon

app = FastAPI()

app.include_router(shakespearean_pokemon.router)
