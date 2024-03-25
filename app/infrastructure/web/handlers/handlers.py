from sanic import Sanic, SanicException
from app.domain.shared.shared_errors import DomainError
from app.infrastructure.system.error.utils.handler.error_handler import app_error_handler, catch_all_error_handler, sanic_error_handler

def setup_handlers(app:Sanic):
    """Registers middleware functions with the Sanic app."""
    app.error_handler.add(SanicException, sanic_error_handler)
    app.error_handler.add(DomainError, app_error_handler)
    app.error_handler.add(Exception, catch_all_error_handler)