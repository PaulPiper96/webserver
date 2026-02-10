from fastapi import FastAPI

from app.api.v1.user import router as user_router
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI()

    # Routes
    app.include_router(user_router, prefix="/api/v1")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def root():
        return {"hello": "fastapi"}

    return app


app = create_app()