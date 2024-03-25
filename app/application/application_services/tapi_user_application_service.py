from app.application.events.etos.eto import Event
from app.application.events.event_publisher_interfaces.tapi_user_event_publisher_interface import IUserEventPublisher
from app.application.use_cases.use_case_interfaces.tapi_user_service_interface import IUserUseCase
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List

from app.domain.shared.shared_errors import DomainError, ErrorType

class UserApplicationService:
    def __init__(self, user_use_case: IUserUseCase, user_event_publisher: IUserEventPublisher):
        self.user_use_case = user_use_case
        self.user_event_publisher = user_event_publisher

    def create_user(self, user_dto: UserCreateDTO,current_user_reference:str) -> str:
        """
        Creates a new user based on the provided UserCreateDTO after ensuring 
        no user exists with the same email. Reports conflict if a user already exists.

        Args:
            user_dto (UserCreateDTO): DTO containing the user data.

        Returns:
            str: The reference ID of the created user.

        Raises:
            DomainError: If a user with the provided email already exists.
        """
        # Check if a user with the same email already exists
        existing_user = self.user_use_case.get_user_by_email(user_dto.email)
        current_user = self.user_use_case.get_user_by_reference(current_user_reference)
        if not current_user:
            # If the user exists, raise a conflict error
            raise DomainError(ErrorType.UnAuthorized, "You are not authorized to create a user")
        
        if existing_user:
            # If the user exists, raise a conflict error
            raise DomainError(ErrorType.ConflictError, f"A user with the email {user_dto.email} already exists.")
        
        # Proceed with user creation if no existing user was found
        user_reference =self.user_use_case.create_user(user_dto,current_user_reference)
        
        user_created_event = Event('UserCreatedEvent', "UserEvent",current_user_reference,user_dto.to_dict()).serialize()
        
        self.user_event_publisher.publish_user_created_event(user_created_event)
        
        return user_reference
        
        
       

    def update_user(self, user_reference: str, user_dto: UserUpdateDTO,current_user_reference) -> str:
        """
        Update an existing user based on the provided UserUpdateDTO.

        Args:
            user_reference (str): The reference ID of the user to be updated.
            user_dto (UserUpdateDTO): DTO containing updated user data.

        Returns:
            str: The reference ID of the updated user.
        """
        current_user = self.user_use_case.get_user_by_reference(current_user_reference)
        if not current_user:
            # If the user exists, raise a conflict error
            raise DomainError(ErrorType.UnAuthorized, "You are not authorized to create a user")
        
        return self.user_use_case.update_user(user_reference, user_dto,current_user_reference)

    def get_user_by_reference(self, user_reference: str) -> User:
        """
        Retrieve a user by its reference ID.

        Args:
            user_reference (str): The reference ID of the user to retrieve.

        Returns:
            User: The retrieved user object.
        """
        return self.user_use_case.get_user_by_reference(user_reference)

    def get_all_users(self, page: int) -> List[User]:
        """
        Retrieve all users, paginated.

        Args:
            page (int): The page number of the user list to retrieve.

        Returns:
            List[User]: A list of User objects on the specified page.
        """
        return self.user_use_case.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        """
        Delete a user permanently.

        Args:
            user_reference (str): The reference ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        return self.user_use_case.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        """
        Soft delete a user, marking it as inactive or deleted without permanently removing it.

        Args:
            user_reference (str): The reference ID of the user to soft delete.

        Returns:
            bool: True if the user was successfully soft deleted, False otherwise.
        """
        return self.user_use_case.soft_delete_user(user_reference)

   