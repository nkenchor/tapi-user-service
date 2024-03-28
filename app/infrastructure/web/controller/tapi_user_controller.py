from sanic import HTTPResponse, Request
from sanic.response import json

from app.application.application_services.tapi_user_application_service import (
    UserApplicationService,
)
from app.domain.dtos.tapi_user_create import UserCreateDTO
from app.domain.dtos.tapi_user_organisation import UserAddOrganisationDTO, UserRemoveOrganisationDTO
from app.domain.dtos.tapi_user_update import UserUpdateDTO
from app.domain.shared.shared_validation import validator
from app.domain.shared.shared_errors import DomainError, ErrorType
from sanic_ext import openapi

from app.infrastructure.system.error.setup.infrastructure_errors import (
    InfrastructureError,
)


class UserController:
    def __init__(self, user_application_service: UserApplicationService):
        self.user_application_service = user_application_service

    @openapi.summary("Create a new user")
    @openapi.description(
        "Creates a new user with the provided details. Returns the user's unique reference ID upon success."
    )
    @openapi.body(
    {
        "application/json": {
            "example": {
                "user_reference": "123e4567-e89b-12d3-a456-426614174000",
                "email": "mike.doe@example.com"
            }
        }
        },
        description="The details of the user to be created, including name, email, and password.",
        required=True,
    )
    @openapi.response(
        201,
        {
            "application/json": {
                "example": {"user_reference": "123e4567-e89b-12d3-a456-426614174000"}
            }
        },
        description="User successfully created. Returns the unique reference ID of the new user.",
    )
    @openapi.response(
        400,
        {
            "application/json": {
                "example": {
                    "error_reference": "123e4567-e89b-12d3-a456-426614174000",
                    "error_type": "VALIDATION_ERROR",
                    "errors": ["Email is invalid"],
                    "status_code": 400,
                    "timestamp": "2023-01-01T12:00:00Z",
                }
            }
        },
        description="Validation error occurred with the provided data.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "123e4567-e89b-12d3-a456-426614174000",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["An unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2023-01-01T12:00:00Z",
                }
            }
        },
        description="Internal server error.",
    )
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
            validator.validate(data)

            # Assuming the request JSON directly maps to UserCreateDTO's structure.
            user_dto = UserCreateDTO(**data)
            user_ref_id = self.user_application_service.create_user(
                user_dto
            )
            return json({"user_reference": user_ref_id}, status=201)

        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()

    @openapi.summary("Update an existing user")
    @openapi.description(
        "Updates user details for the user with the specified user reference. All fields are optional, but at least one must be provided."
    )
    @openapi.body(
        {
            "application/json": {
                "example": {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "mobile_number": "+440987654321",
                    "consent_preferences": {
                        "marketing_emails": True,
                        "third_party_data_sharing": False,
                        "cookies_acceptance": True,
                        "personalized_ads": True,
                        "analytics_tracking": True,
                        "location_tracking": False,
                        "push_notifications": True,
                        "privacy_policy": True,
                        "terms_and_conditions": True
                    }
                    }
            }
        },
        description="Optional fields to update for the user, including first name, last name, mobile number, and consent.",
        required=True,
    )
    @openapi.response(
         200,
        {
            "application/json": {
                "example": {"user_reference": "123e4567-e89b-12d3-a456-426614174000"}
            }
        },
        description="User successfully updated. Returns the unique reference ID of the new user.",
    )
    @openapi.response(
        400,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "VALIDATION_ERROR",
                    "errors": ["Email format is invalid"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Validation error occurred with the provided data.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    @openapi.tag("Users")
    @openapi.operation("update_user")
    async def update_user(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            current_user_reference = request.headers.get("X-User-Reference")
            if not current_user_reference:
                return InfrastructureError(
                    ErrorType.UnAuthorized, "Unauthorised user"
                ).to_response()

            data = request.json
            # Use the validator to validate incoming data
            validator.validate(data)

            user_dto = UserUpdateDTO(**data)
            user_ref_id = self.user_application_service.update_user(
                user_reference, user_dto, current_user_reference
            )
            return json({"user_reference": user_ref_id}, status=200)

        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()


    @openapi.summary("Add a user to an organisation")
    @openapi.description(
        "Adds a user to an organisation with the specified user reference."
    )
    @openapi.body(
        {
            "application/json": {
                "example": {
                    "organisation": "Palms Consulting",
    
                }
            }
        },
        description="Add user to organisation",
        required=True,
    )
    @openapi.response(
         200,
        {
            "application/json": {
                "example": {"user_reference": "123e4567-e89b-12d3-a456-426614174000"}
            }
        },
        description="User successfully updated with an organisation. Returns the unique reference ID of the new user.",
    )
    @openapi.response(
        400,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "VALIDATION_ERROR",
                    "errors": ["Email format is invalid"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Validation error occurred with the provided data.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    @openapi.tag("Users")
    @openapi.operation("add_user_to_organisation")
    async def add_user_to_organisation(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            current_user_reference = request.headers.get("X-User-Reference")
            if not current_user_reference:
                return InfrastructureError(
                    ErrorType.UnAuthorized, "Unauthorised user"
                ).to_response()

            data = request.json
            # Use the validator to validate incoming data
            validator.validate(data)

            user_organisation_dto = UserAddOrganisationDTO(**data)
            user_ref_id = self.user_application_service.add_user_to_organisation(
                user_reference, user_organisation_dto, current_user_reference
            )
            return json({"user_reference": user_ref_id}, status=200)

        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()
            
    @openapi.summary("Remove a user to an organisation")
    @openapi.description(
        "Removes a user from an organisation with the specified user reference."
    )
    @openapi.body(
        {
            "application/json": {
                "example": {
                    "organisation": "Palms Consulting",
    
                }
            }
        },
        description="Remove user to organisation",
        required=True,
    )
    @openapi.response(
         200,
        {
            "application/json": {
                "example": {"user_reference": "123e4567-e89b-12d3-a456-426614174000"}
            }
        },
        description="User successfully removed from the organisation. Returns the unique reference ID of the  user.",
    )
    @openapi.response(
        400,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "VALIDATION_ERROR",
                    "errors": ["Email format is invalid"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Validation error occurred with the provided data.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    @openapi.tag("Users")
    @openapi.operation("remove_user_from_organisation")
    async def remove_user_from_organisation(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            current_user_reference = request.headers.get("X-User-Reference")
            if not current_user_reference:
                return InfrastructureError(
                    ErrorType.UnAuthorized, "Unauthorised user"
                ).to_response()

            data = request.json
            # Use the validator to validate incoming data
            validator.validate(data)

            user_organisation_dto = UserRemoveOrganisationDTO(**data)
            user_ref_id = self.user_application_service.remove_user_from_organisation(
                user_reference, user_organisation_dto, current_user_reference
            )
            return json({"user_reference": user_ref_id}, status=200)

        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()
            
            
            
    @openapi.summary("Get user details")
    @openapi.description(
        "Retrieves the details of a specific user by their unique reference ID."
    )
    @openapi.tag("Users")
    @openapi.operation("get_user_by_reference")
    @openapi.response(
        200,
        {
            "application/json": {
                "example": {
                    "user_reference": "01ef9f9c-6671-406f-a388-93c9d1c7ca78",
                    "first_name": "Felix",
                    "last_name": "Dowin",
                    "full_name": "Felix Dowin",
                    "mobile_number": "+447876042778",
                    "email": "felix.doe@example.com",
                    "organisations": [],
                    "is_verified_email": False,
                    "is_verified_phone": False,
                    "is_active": True,
                    "created_at_timestamp": "2024-03-26T21:38:47.247911",
                    "updated_at_timestamp": "2024-03-26T21:50:27.065421",
                    "consent_preferences": {
                        "marketing_emails": True,
                        "third_party_data_sharing": False,
                        "cookies_acceptance": True,
                        "personalized_ads": True,
                        "analytics_tracking": True,
                        "location_tracking": False,
                        "push_notifications": True,
                        "privacy_policy": True,
                        "terms_and_conditions": True
                    }
                }
            }
        },
        description="The details of the user.",
    )
    @openapi.response(
        404,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "NOT_FOUND_ERROR",
                    "errors": ["User not found"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="User with the given reference ID does not exist.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    async def get_user_by_reference(
        self, request: Request, user_reference: str
    ) -> HTTPResponse:
        try:
            user = self.user_application_service.get_user_by_reference(user_reference)
            return json(user.to_json(), status=200)
        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()

    @openapi.summary("Get current user details")
    @openapi.description("Retrieves the details of the current user using the X-User-Reference header.")
    @openapi.tag("Users")
    @openapi.operation("get_current_user_by_reference")
    @openapi.parameter("X-User-Reference", str, location="header", description="The unique reference ID of the current user.", required=True)
    @openapi.response(
        200,
        {
            "application/json": {
                "example": {
                    "user_reference": "01ef9f9c-6671-406f-a388-93c9d1c7ca78",
                    "first_name": "Felix",
                    "last_name": "Dowin",
                    "full_name": "Felix Dowin",
                    "mobile_number": "+447876042778",
                    "email": "felix.doe@example.com",
                    "organisations": [],
                    "is_verified_email": False,
                    "is_verified_phone": False,
                    "is_active": True,
                    "created_at_timestamp": "2024-03-26T21:38:47.247911",
                    "updated_at_timestamp": "2024-03-26T21:50:27.065421",
                    "consent_preferences": {
                        "marketing_emails": True,
                        "third_party_data_sharing": False,
                        "cookies_acceptance": True,
                        "personalized_ads": True,
                        "analytics_tracking": True,
                        "location_tracking": False,
                        "push_notifications": True,
                        "privacy_policy": True,
                        "terms_and_conditions": True
                    }
                }
            }
        },
        description="The details of the user.",
    )
    @openapi.response(
        404,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "NOT_FOUND_ERROR",
                    "errors": ["User not found"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="User with the given reference ID does not exist.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    async def get_current_user(self, request: Request) -> HTTPResponse:
        try:
            current_user_reference = request.headers.get("X-User-Reference")
            if not current_user_reference:
                return InfrastructureError(
                    ErrorType.NotFound, "No current user"
                ).to_response()

            user = self.user_application_service.get_user_by_reference(
                current_user_reference
            )
            return json(user.to_json(), status=200)
        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()

    @openapi.summary("List all users")
    @openapi.description(
        "Returns a list of all users, paginated by the specified page number."
    )
    @openapi.tag("Users")
    @openapi.operation("get_all_users")
    @openapi.response(
        200,
        {
            "application/json": {
                "example": [
                        {
                        "user_reference": "01ef9f9c-6671-406f-a388-93c9d1c7ca78",
                        "first_name": "Felix",
                        "last_name": "Dowin",
                        "full_name": "Felix Dowin",
                        "mobile_number": "+447876042778",
                        "email": "felix.doe@example.com",
                        "organisations": [],
                        "is_verified_email": False,
                        "is_verified_phone": False,
                        "is_active": True,
                        "created_at_timestamp": "2024-03-26T21:38:47.247911",
                        "updated_at_timestamp": "2024-03-26T21:50:27.065421",
                        "consent_preferences": {
                            "marketing_emails": True,
                            "third_party_data_sharing": False,
                            "cookies_acceptance": True,
                            "personalized_ads": True,
                            "analytics_tracking": True,
                            "location_tracking": False,
                            "push_notifications": True,
                            "privacy_policy": True,
                            "terms_and_conditions": True
                        }
                    }
                ]
            }
        },
        description="The details of the users.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    async def get_all_users(self, request: Request, page: int) -> HTTPResponse:
        try:
            users = self.user_application_service.get_all_users(page)
            users_json = [user.to_json() for user in users]
            return json(users_json, status=200)
        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()

    @openapi.summary("Delete a user")
    @openapi.description("Deletes a specific user by their unique reference ID.")
    @openapi.tag("Users")
    @openapi.operation("delete_user")
    @openapi.response(
        200,
        {
            "application/json": {
                "example": {"user_reference": "123e4567-e89b-12d3-a456-426614174000"}
            }
        },
        description="User successfully deleted. Returns the unique reference ID of the deleted user.",
    )
    @openapi.response(
        404,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-67890",
                    "error_type": "NOT_FOUND_ERROR",
                    "errors": ["User not found"],
                    "status_code": 400,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="User with the given reference ID does not exist.",
    )
    @openapi.response(
        500,
        {
            "application/json": {
                "example": {
                    "error_reference": "unique-error-id-12345",
                    "error_type": "INTERNAL_ERROR",
                    "errors": ["Unexpected error occurred"],
                    "status_code": 500,
                    "timestamp": "2024-03-25T10:30:00.000Z",
                }
            }
        },
        description="Internal server error.",
    )
    async def delete_user(self, request: Request, user_reference: str) -> HTTPResponse:
        try:
            result = self.user_application_service.delete_user(user_reference)
            if result:
                return json({"message": "User deleted successfully"}, status=200)
            else:
                return json({"message": "User not found"}, status=404)
        except DomainError as domain_error:
            # Handle domain-specific errors with proper HTTP response
            return InfrastructureError.from_domain_error(domain_error).to_response()

        except Exception as e:
            # Catch-all for any other unexpected errors
            return InfrastructureError(
                ErrorType.InternalError, f"Unexpected error - {str(e)}"
            ).to_response()
