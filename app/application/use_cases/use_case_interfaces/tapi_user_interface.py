from abc import ABC, abstractmethod
from typing import List
from app.domain.dtos.tapi_user_create import UserCreateDTO
from app.domain.dtos.tapi_user_organisation import UserAddOrganisationDTO, UserRemoveOrganisationDTO
from app.domain.dtos.tapi_user_update import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User


class IUserUseCase(ABC):
    @abstractmethod
    def create_user(self, user_dto: UserCreateDTO) -> str:
        """Create a new user."""
        pass

    @abstractmethod
    def update_user(
        self, user_reference: str, user_dto: UserUpdateDTO, current_user_reference: str
    ) -> str:
        """Update an existing user."""
        pass
    
    @abstractmethod
    def add_user_to_organisation(
        self, user_reference: str, user_dto: UserAddOrganisationDTO, current_user_reference: str
    ) -> str:
        """Update an existing user."""
        pass

    @abstractmethod
    def get_user_by_reference(self, user_reference: str) -> User:
        """Retrieve a user by its reference."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        """Retrieve a user by its email."""
        pass

    @abstractmethod
    def get_all_users(self, page: int) -> List[User]:
        """
        Retrieve a paginated list of all users.

        Parameters:
            page (int): The page number to retrieve.

        Returns:
            List[User]: A list of User objects.
        """
        pass

    @abstractmethod
    def delete_user(self, user_reference: str) -> bool:
        """
        Delete a user permanently.

        Parameters:
            user_reference (str): The reference of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def soft_delete_user(self, user_reference: str) -> bool:
        """
        Soft delete a user.

        Parameters:
            user_reference (str): The reference of the user to soft delete.

        Returns:
            bool: True if the user was successfully soft deleted, False otherwise.
        """
        pass

    @abstractmethod
    def remove_user_from_organisation(
        self, user_reference: str, organisation_remove_dto: UserRemoveOrganisationDTO, current_user_reference: str
    ) -> str:
        """Update an existing user."""
        pass