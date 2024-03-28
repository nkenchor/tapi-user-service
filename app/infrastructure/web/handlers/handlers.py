from sanic import Sanic
from app.infrastructure.system.error.utils.handler.error_handler import (

    catch_all_error_handler,

)


def setup_handlers(app: Sanic):
    """Registers middleware functions with the Sanic app."""

    app.error_handler.add(Exception, catch_all_error_handler)
