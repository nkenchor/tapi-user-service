from sanic.request import Request




from app.domain.shared.shared_errors import ErrorType
from app.infrastructure.system.error.setup.infrastructure_errors import InfrastructureError



from sanic.exceptions import (
    NotFound,
    MethodNotAllowed,
    Forbidden,
    Unauthorized,
    SanicException,
)


async def catch_all_error_handler(request: Request, exception):
    # Determine the error type and message based on the exception
    if isinstance(exception, NotFound):
        error_type = ErrorType.NotFound
        message = f"Resource not found: {request.path}"
    elif isinstance(exception, MethodNotAllowed):
        error_type = ErrorType.MethodNotAllowed
        message = f"Method not allowed: {request.method} for {request.path}"
    elif isinstance(exception, Forbidden):
        error_type = ErrorType.Forbidden
        message = "You don't have permission to access this resource."
    elif isinstance(exception, Unauthorized):
        error_type = ErrorType.Unauthorized
        message = "Authentication is required to access this resource."
    elif isinstance(exception, SanicException):
        # Handle other Sanic-specific exceptions
        error_type = ErrorType.BadRequest
        message = f"Bad request: {str(exception)}"
    else:
        # Default case for unexpected or non-Sanic exceptions
        error_type = ErrorType.ServerError
        message = f"Unhandled exception: {str(exception)}"

    # Create and return the custom error response
    return InfrastructureError(error_type=error_type, message=message).to_response()
