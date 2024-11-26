from fastapi import FastAPI, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import v1

def create_app() -> FastAPI:
    _app = FastAPI(
        title="SSHFull",
        description="",
        version='0.1.0',
        docs_url='/',
        redoc_url='/docs',
    )

    _app.include_router(v1)

    _app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = create_app()