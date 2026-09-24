"""Application configuration and constants."""

from __future__ import annotations

# HTTP origins allowed to call the API from the browser.
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Ports used by each service.
API_PORT = 8000
WEB_PORT = 3000
