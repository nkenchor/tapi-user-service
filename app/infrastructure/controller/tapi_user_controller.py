from sanic import HTTPResponse, Request
from sanic.response import json

from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.domain.dtos.tapi_user_create_dto import  UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO
from app.domain.validation.tapi_user_validation import  ValidationError, validator
from framework.error.setup.error_setup import AppError, ErrorType
from sanic_ext import openapi

class UserController:
    def __init__(self, user_application_service: UserApplicationService):
        self.user_application_service = user_application_service
    @openapi.summary("Create a new user")
    @openapi.description("Creates a new user with the provided details. Returns the user's unique reference ID upon success.")
    @openapi.body({"application/json": {"example": {"first_name": "John","last_name": "Doe","mobile_no":"+447674532289", "email": "john.doe@example.com"}}}, description="The details of the user to be created, including name, email, and password.", required=True)
    @openapi.response(201, {"application/json": {"example": {"userReference": "123e4567-e89b-12d3-a456-426614174000"}}}, description="User successfully created. Returns the unique reference ID of the new user.")
    @openapi.response(400, {"application/json": {"example": {"error_reference": "123e4567-e89b-12d3-a456-426614174000", "error_type": "VALIDATION_ERROR", "errors": ["Email is invalid"], "status_code": 400, "timestamp": "2023-01-01T12:00:00Z"}}}, description="Validation error occurred with the provided data.")
    @openapi.response(500, {"application/json": {"example": {"error_reference": "123e4567-e89b-12d3-a456-426614174000", "error_type": "INTERNAL_ERROR", "errors": ["An unexpected error occurred"], "status_code": 500, "timestamp": "2023-01-01T12:00:00Z"}}}, description="Internal server error.")
    @openapi.tag("Users")
    @openapi.operation("create_user")
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
   
    @openapi.summary("Update an existing user")
    @openapi.description("Updates user details for the user with the specified user reference. All fields are optional, but at least one must be provided.")
    @openapi.body({"application/json": {"example": {"first_name": "Jane", "last_name": "Doe", "mobile_number": "0987654321", "email": "jane.doe@example.com"}}}, description="Optional fields to update for the user, including first name, last name, mobile number, and email.", required=True)
    @openapi.response(200, {"application/json": {"example": {"message": "User updated successfully"}}}, description="The user was successfully updated.")
    @openapi.response(400, {"application/json": {"example": {"error_reference": "unique-error-id-67890", "error_type": "VALIDATION_ERROR", "errors": ["Email format is invalid"], "status_code": 400, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="Validation error occurred with the provided data.")
    @openapi.response(500, {"application/json": {"example": {"error_reference": "unique-error-id-12345", "error_type": "INTERNAL_ERROR", "errors": ["Unexpected error occurred"], "status_code": 500, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="Internal server error.")
    @openapi.tag("Users")
    @openapi.operation("update_user")
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

    @openapi.summary("Get user details")
    @openapi.description("Retrieves the details of a specific user by their unique reference ID.")
    @openapi.tag("Users")
    @openapi.operation("get_user_by_reference")
    @openapi.response(200, {"application/json": {"example": {
        "user_reference": "unique-user-id-123",
        "first_name": "John",
        "last_name": "Doe",
        "mobile_number": "1234567890",
        "email": "john.doe@example.com",
        "organisations": [],
        "notification_options": {},
        "is_verified_email": True,
        "is_verified_phone": False,
        "is_active": True,
        "date_of_birth": "1990-01-01",
        "last_login_timestamp": "2024-03-25T12:00:00.000Z",
        "last_updated_timestamp": "2024-03-25T12:00:00.000Z",
        "updated_by_user_reference": "",
        "consent_preferences": {}
    }}}, description="The details of the user.")
    @openapi.response(404, {"application/json": {"example": {"error_reference": "unique-error-id-67890", "error_type": "NOT_FOUND_ERROR", "errors": ["User not found"], "status_code": 400, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="User with the given reference ID does not exist.")
    @openapi.response(500, {"application/json": {"example": {"error_reference": "unique-error-id-12345", "error_type": "INTERNAL_ERROR", "errors": ["Unexpected error occurred"], "status_code": 500, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="Internal server error.")
    async def get_user_by_reference(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            user = self.user_application_service.get_user_by_reference(user_reference)
            return json(user.serialize(), status=200)
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()


    @openapi.summary("List all users")
    @openapi.description("Returns a list of all users, paginated by the specified page number.")
    @openapi.tag("Users")
    @openapi.operation("get_all_users")
    @openapi.response(200, {"application/json": {"example": [{
        "user_reference": "unique-user-id-123",
        "first_name": "John",
        "last_name": "Doe",
        "mobile_number": "1234567890",
        "email": "john.doe@example.com",
        "organisations": [],
        "notification_options": {},
        "is_verified_email": True,
        "is_verified_phone": False,
        "is_active": True,
        "date_of_birth": "1990-01-01",
        "last_login_timestamp": "2024-03-25T12:00:00.000Z",
        "last_updated_timestamp": "2024-03-25T12:00:00.000Z",
        "updated_by_user_reference": "",
        "consent_preferences": {}
    }]}}, description="The details of the users.")
    @openapi.response(500, {"application/json": {"example": {"error_reference": "unique-error-id-12345", "error_type": "INTERNAL_ERROR", "errors": ["Unexpected error occurred"], "status_code": 500, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="Internal server error.")
    async def get_all_users(self, request: Request, page: int) -> HTTPResponse:
        try:
            users = self.user_application_service.get_all_users(page)
            users_json = [user.serialize() for user in users]
            return json(users_json, status=200)
        except AppError as app_error:
            return app_error.to_response()
        except Exception as e:
            return AppError(ErrorType.InternalError, f"Unexpected error: {str(e)}").to_response()

    @openapi.summary("Delete a user")
    @openapi.description("Deletes a specific user by their unique reference ID.")
    @openapi.tag("Users")
    @openapi.operation("delete_user")    
    @openapi.response(200, {"application/json": {"example": {"userReference": "123e4567-e89b-12d3-a456-426614174000"}}}, description="User successfully deleted. Returns the unique reference ID of the deleted user.")
    @openapi.response(404, {"application/json": {"example": {"error_reference": "unique-error-id-67890", "error_type": "NOT_FOUND_ERROR", "errors": ["User not found"], "status_code": 400, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="User with the given reference ID does not exist.")
    @openapi.response(500, {"application/json": {"example": {"error_reference": "unique-error-id-12345", "error_type": "INTERNAL_ERROR", "errors": ["Unexpected error occurred"], "status_code": 500, "timestamp": "2024-03-25T10:30:00.000Z"}}}, description="Internal server error.")
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
