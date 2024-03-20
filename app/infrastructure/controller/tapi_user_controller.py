from sanic import HTTPResponse, Request
from sanic.response import json

from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO
from app.domain.validation.tapi_user_validation import TypeBasedValidator, ValidationError, validator
from framework.error.setup.error_setup import AppError, ErrorType
from sanic_openapi import doc

class UserController:
    def __init__(self, user_application_service: UserApplicationService):
        self.user_application_service = user_application_service


    @doc.summary("Creates a new user")
    @doc.description("This endpoint allows for creating a new user in the system.")
    @doc.consumes(doc.JsonBody({"username": str, "email": str, "password": str}), location="body")
    @doc.produces({"userReference": str}, description="The reference ID of the created user", content_type="application/json")

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
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()
      

    async def update_user(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            data = request.json
            # Assuming you have a UserUpdateDTO and corresponding validation
            user_dto = UserUpdateDTO(**data)
            self.user_application_service.update_user(user_reference, user_dto)
            return json({"message": "User updated successfully"}, status=200)
        except ValidationError as ve:
            raise AppError(ErrorType.ValidationError, str(ve))
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()

    async def get_user_by_reference(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            user = self.user_application_service.get_user_by_reference(user_reference)
            return json(user.serialize(), status=200)
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()


    async def get_all_users(self, request: Request, page: int) -> HTTPResponse:
        try:
            users = self.user_application_service.get_all_users(page)
            users_json = [user.serialize() for user in users]
            return json(users_json, status=200)
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()


    async def delete_user(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            result = self.user_application_service.delete_user(user_reference)
            if result:
                return json({"message": "User deleted successfully"}, status=200)
            else:
                return json({"message": "User not found"}, status=404)
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()
