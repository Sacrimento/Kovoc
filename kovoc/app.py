from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from kovoc.api.routers import quizz, vocabulary
from kovoc.utils.settings import get_settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        get_settings()
    except ValidationError as exc:
        raise ValueError(
            "Settings could not be loaded, check your environments variables"
        ) from exc

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(vocabulary.router)
app.include_router(quizz.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
