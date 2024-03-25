from sanic.request import Request
from sanic.exceptions import SanicException



from app.domain.shared.shared_errors import DomainError, ErrorType
from app.infrastructure.system.error.setup.infrastructure_errors import InfrastructureError



async def sanic_error_handler(request: Request, exception: SanicException):
    return InfrastructureError(error_type=ErrorType.NotFound, message=f"Resource not found - {str(exception)}").to_response()
    # await log_error_handler(request, exception)
   

async def app_error_handler(request, exception: DomainError):
    return InfrastructureError.from_domain_error(exception).to_response()

async def catch_all_error_handler(request, exception):
    return InfrastructureError(error_type=ErrorType.ServerError,  message=f"Unhandled exception - {str(exception)}").to_response()
