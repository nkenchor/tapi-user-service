
from sanic.response import json
from sanic.exceptions import SanicException

from framework.error.setup.error_setup import AppError, ErrorType, error_message



async def error_middleware(request, exception):
    if isinstance(exception, AppError):
        return json({
            "errorReference": exception.error_reference,
            "errorType": exception.error_type.value,  # Assuming ErrorType is an Enum
            "timeStamp": exception.time_stamp,
            "code": exception.status_code,
            "errors": [str(exception)]
        }, status=exception.status_code)
    elif isinstance(exception, SanicException):
        # Handling Sanic built-in exceptions
        error_response = error_message(ErrorType.InternalError, str(exception))
        return json({
            "errorReference": error_response.error_reference,
            "errorType": error_response.error_type.value,
            "timeStamp": error_response.time_stamp,
            "code": error_response.code,
            "errors": [error_response.errors]
        }, status=error_response.code)
    else:
        # Fallback for unhandled errors
        print(f"Unhandled Error: {exception}")
        fallback_error = error_message(ErrorType.InternalError, "Internal server error")
        return json({
            "errorReference": fallback_error.error_reference,
            "errorType": fallback_error.error_type.value,
            "timeStamp": fallback_error.time_stamp,
            "code": fallback_error.code,
            "errors": fallback_error.errors
        }, status=fallback_error.code)
