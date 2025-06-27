import asyncio
import logging

from api.v1.router import v1_router
from core.config import app_config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.exceptions_mapper import HTTPExceptionsMapper

app = FastAPI()
app.include_router(v1_router)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=app_config.media_path), name="media")

HTTPExceptionsMapper(app, logging.getLogger(__name__)).setup_handlers()


async def main():
    server_cfg = uvicorn.Config(
        "main:app", port=app_config.server.port, host="0.0.0.0", log_level="info"
    )
    server = uvicorn.Server(server_cfg)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
