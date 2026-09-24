"""FastAPI application entry point for the Shop OOP system."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import products_router, customers_router, cart_router
from config import ALLOWED_ORIGINS
from store import seed_data


def create_app() -> FastAPI:
    """Build and configure the application."""
    app = FastAPI(title="Shop OOP API", version="1.0.0")

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        """Return a lightweight readiness response for local tooling."""
        return {"status": "ok"}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(products_router)
    app.include_router(customers_router)
    app.include_router(cart_router)

    seed_data()
    return app


app = create_app()