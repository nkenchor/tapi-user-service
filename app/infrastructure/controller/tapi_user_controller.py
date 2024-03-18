from sanic import HTTPResponse, Request
from sanic.response import json

from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.validation.tapi_user_validation import TypeBasedValidator, ValidationError, validator
from framework.error.setup.error_setup import AppError, ErrorType

class UserController:
    def __init__(self, user_application_service: UserApplicationService):
        self.user_application_service = user_application_service

    async def create_user(self, request: Request) -> HTTPResponse:
        """
        Sanic endpoint to create a new user.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            HTTPResponse: The response to the client.
        """
        try:
            data = request.json

            # Use the validator to validate incoming data
            try:
                validator.validate(data)
            except ValidationError as ve:
                # Convert ValidationError to AppError for consistency
                raise AppError(ErrorType.ValidationError, str(ve))
            
            # Assuming the request JSON directly maps to UserCreateDTO's structure.
            user_dto = UserCreateDTO(**request.json)
            user_ref_id = self.user_application_service.create_user(user_dto)
            return json({"userReference": user_ref_id}, status=201)
        except AppError as app_error:
            # Handle application-specific errors
            return app_error.to_response()
        except Exception as e:
            # Catch-all for any other unexpected errors
            # Consider logging the exception here for debugging purposes
            general_error = AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}")
            return general_error.to_response()
