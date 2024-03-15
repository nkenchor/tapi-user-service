from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import SanicException

import json

from framework.error.setup.error_setup import AppError, ErrorType

async def sanic_exception_handler(request: Request, exception: SanicException):
    app_error = AppError(ErrorType.NotFound, f"Resource not found: {str(exception)}")
    # await log_error_handler(request, exception)
    return app_error.to_response()

async def app_error_handler(request, exception: AppError):
    error_response = json.loads(exception.to_json())
    # await log_error_handler(request, exception)
    return HTTPResponse(status=error_response['statusCode'], body=exception.to_json())

async def catch_all_exception_handler(request, exception):
    app_error = AppError(ErrorType.ServerError, f"Unhandled exception: {str(exception)}")
    # await log_error_handler(request, exception)
    return app_error.to_response()
