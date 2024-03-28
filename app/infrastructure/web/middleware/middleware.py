from sanic import Sanic
from app.infrastructure.system.logger.middleware.logger_middleware import (
    log_middleware,
    request_middleware,
)


def setup_middleware(app: Sanic):
    """Registers middleware functions with the Sanic app."""
    app.request_middleware.append(request_middleware)
    app.response_middleware.append(log_middleware)
